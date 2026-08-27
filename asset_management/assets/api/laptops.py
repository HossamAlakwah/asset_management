from django.utils import timezone
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.models import Laptop, LaptopLog, LaptopStorage

from .excel import Column, ExcelIOMixin
from .stock import StockOnCreateMixin

EXCEL_COLUMNS = [
    Column("Product", "product", required=True),
    Column("Serial", "serial", required=True),
    Column("CPU", "cpu"),
    Column("CPU Generation", "cpu_generation"),
    Column("RAM", "ram"),
    Column("Status", "status"),
    Column("Warranty", "warranty"),
    Column("On Hand Date", "on_hand_date"),
    Column("Return Date", "return_date"),
    Column("Comments", "comments"),
    Column(
        "Employee Email",
        "employee",
        source="employee.email",
        lookup=("assets.Employee", "email"),
    ),
    Column("Branch", "branch", source="branch.name", lookup=("assets.Branch", "name")),
]


class LaptopStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaptopStorage
        fields = ("id", "type", "size")
        read_only_fields = ("id",)


class LaptopLogSerializer(serializers.ModelSerializer):
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
        model = LaptopLog
        fields = (
            "id",
            "old_status",
            "new_status",
            "old_employee",
            "old_employee_name",
            "new_employee",
            "new_employee_name",
            "on_hand_date",
            "return_date",
            "branch",
            "branch_name",
            "changed_by",
            "changed_by_username",
            "change_time",
        )
        read_only_fields = fields


class LaptopSerializer(StockOnCreateMixin, serializers.ModelSerializer):
    storage_devices = LaptopStorageSerializer(many=True, required=False)
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    employee_name = serializers.CharField(source="employee.name", read_only=True)
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    logs = LaptopLogSerializer(many=True, read_only=True)

    class Meta:
        model = Laptop
        fields = (
            "id",
            "product",
            "serial",
            "cpu",
            "cpu_generation",
            "ram",
            "status",
            "employee",
            "employee_name",
            "warranty",
            "on_hand_date",
            "return_date",
            "comments",
            "branch",
            "branch_name",
            "storage_devices",
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

    def create(self, validated_data):
        storage = validated_data.pop("storage_devices", [])
        laptop = super().create(validated_data)
        for item in storage:
            LaptopStorage.objects.create(laptop=laptop, **item)
        return laptop

    def update(self, instance, validated_data):
        storage = validated_data.pop("storage_devices", None)
        request = self.context.get("request")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if request:
            instance._changed_by = request.user
        instance.save()
        if storage is not None:
            instance.storage_devices.all().delete()
            for item in storage:
                LaptopStorage.objects.create(laptop=instance, **item)
        return instance


class LaptopViewSet(ExcelIOMixin, viewsets.ModelViewSet):
    queryset = Laptop.objects.select_related(
        "branch", "employee", "created_by"
    ).prefetch_related(
        "storage_devices",
        "logs__changed_by",
        "logs__old_employee",
        "logs__new_employee",
        "logs__branch",
    )
    serializer_class = LaptopSerializer
    search_fields = ["serial", "product", "employee__name", "employee__email"]
    filterset_fields = ["status", "branch", "employee", "cpu", "ram"]
    ordering_fields = ["created_at", "serial", "product", "status"]
    ordering = ["-created_at"]

    excel_columns = EXCEL_COLUMNS
    excel_sheet_name = "Laptops"

    ui_title = "Laptops"
    ui_group = "Endpoints"
    ui_icon = "laptop"
    ui_list_fields = [
        "serial",
        "product",
        "status",
        "employee_name",
        "branch_name",
        "warranty",
    ]
    ui_log_field = "logs"

    @action(detail=True, methods=["post"])
    def unassign(self, request, pk=None):
        laptop = self.get_object()
        laptop.employee = None
        laptop.status = Laptop.Status.STOCK
        laptop.return_date = timezone.now().date()
        laptop.on_hand_date = None
        laptop._changed_by = request.user
        laptop.save()
        return Response(self.get_serializer(laptop).data)
