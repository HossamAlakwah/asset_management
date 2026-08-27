from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.models import Screen, ScreenLog

from .excel import Column, ExcelIOMixin
from .stock import StockOnCreateMixin

EXCEL_COLUMNS = [
    Column("Product", "product", required=True),
    Column("Serial", "serial", required=True),
    Column("Brand", "brand", required=True),
    Column("Status", "status"),
    Column(
        "Employee Email",
        "employee",
        source="employee.email",
        lookup=("assets.Employee", "email"),
    ),
    Column("Branch", "branch", source="branch.name", lookup=("assets.Branch", "name")),
]


class ScreenLogSerializer(serializers.ModelSerializer):
    changed_by_username = serializers.CharField(
        source="changed_by.username", read_only=True
    )
    old_employee_name = serializers.CharField(
        source="old_employee.name", read_only=True
    )
    new_employee_name = serializers.CharField(
        source="new_employee.name", read_only=True
    )
    branch_name = serializers.CharField(source="branch.name", read_only=True)

    class Meta:
        model = ScreenLog
        fields = (
            "id",
            "old_status",
            "new_status",
            "old_employee",
            "old_employee_name",
            "new_employee",
            "new_employee_name",
            "branch",
            "branch_name",
            "changed_by",
            "changed_by_username",
            "change_time",
        )
        read_only_fields = fields


class ScreenSerializer(StockOnCreateMixin, serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    employee_name = serializers.CharField(source="employee.name", read_only=True)
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    logs = ScreenLogSerializer(many=True, read_only=True)

    class Meta:
        model = Screen
        fields = (
            "id",
            "product",
            "serial",
            "status",
            "brand",
            "employee",
            "employee_name",
            "branch",
            "branch_name",
            "created_at",
            "updated_at",
            "created_by",
            "created_by_username",
            "logs",
        )
        read_only_fields = ("id", "created_at", "updated_at", "created_by")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        view = self.context.get("view")
        if view and getattr(view, "action", None) != "retrieve":
            data.pop("logs", None)
        return data

    def update(self, instance, validated_data):
        request = self.context.get("request")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if request:
            instance._changed_by = request.user
        instance.save()
        return instance


class ScreenViewSet(ExcelIOMixin, viewsets.ModelViewSet):
    queryset = Screen.objects.select_related(
        "branch", "employee", "created_by"
    ).prefetch_related("logs")
    serializer_class = ScreenSerializer
    search_fields = ["serial", "brand", "employee__name", "employee__email"]
    filterset_fields = ["status", "branch", "employee", "product"]
    ordering_fields = ["created_at", "serial", "status"]
    ordering = ["-created_at"]

    excel_columns = EXCEL_COLUMNS
    excel_sheet_name = "Screens"

    ui_title = "Screens"
    ui_group = "Endpoints"
    ui_icon = "desktop"
    ui_list_fields = [
        "serial",
        "product",
        "brand",
        "status",
        "employee_name",
        "branch_name",
    ]
    ui_log_field = "logs"

    @action(detail=True, methods=["post"])
    def unassign(self, request, pk=None):
        screen = self.get_object()
        screen.employee = None
        screen.status = Screen.Status.STOCK
        screen._changed_by = request.user
        screen.save()
        return Response(self.get_serializer(screen).data)
