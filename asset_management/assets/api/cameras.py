from rest_framework import serializers, viewsets

from assets.models import Camera, CameraLog

from .excel import Column, ExcelIOMixin
from .stock import StockOnCreateMixin

EXCEL_COLUMNS = [
    Column("Model", "model", required=True),
    Column("Serial Number", "serial_number", required=True),
    Column("Power Source", "power_source"),
    Column("Location", "location"),
    Column("IP Address", "ip_address"),
    Column("MAC Address", "mac_address"),
    Column("Status", "status"),
    Column("Purchase Date", "purchase_date"),
    Column("Comment", "comment"),
    Column("Branch", "branch", source="branch.name", lookup=("assets.Branch", "name")),
]


class CameraLogSerializer(serializers.ModelSerializer):
    changed_by_username = serializers.CharField(
        source="changed_by.username", read_only=True
    )
    old_branch_name = serializers.CharField(source="old_branch.name", read_only=True)
    new_branch_name = serializers.CharField(source="new_branch.name", read_only=True)

    class Meta:
        model = CameraLog
        fields = (
            "id",
            "old_status",
            "new_status",
            "old_location",
            "new_location",
            "old_branch",
            "old_branch_name",
            "new_branch",
            "new_branch_name",
            "changed_by",
            "changed_by_username",
            "change_time",
            "comment",
        )
        read_only_fields = fields


class CameraSerializer(StockOnCreateMixin, serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    logs = CameraLogSerializer(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = (
            "id",
            "model",
            "serial_number",
            "power_source",
            "location",
            "ip_address",
            "mac_address",
            "status",
            "purchase_date",
            "comment",
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


class CameraViewSet(ExcelIOMixin, viewsets.ModelViewSet):
    queryset = Camera.objects.select_related("branch", "created_by").prefetch_related("logs")
    serializer_class = CameraSerializer
    search_fields = ["serial_number", "model", "ip_address", "mac_address", "location"]
    filterset_fields = ["status", "branch", "power_source"]
    ordering_fields = ["created_at", "serial_number", "model", "status"]
    ordering = ["-created_at"]

    excel_columns = EXCEL_COLUMNS
    excel_sheet_name = "Cameras"

    ui_title = "Cameras"
    ui_group = "Infrastructure"
    ui_icon = "camera"
    ui_list_fields = ["serial_number", "model", "status", "location", "ip_address", "branch_name"]
    ui_log_field = "logs"
