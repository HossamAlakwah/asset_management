from rest_framework import serializers, viewsets

from assets.models import UPS, UPSLog

from .excel import Column, ExcelIOMixin
from .stock import StockOnCreateMixin

EXCEL_COLUMNS = [
    Column("Model", "model", required=True),
    Column("Serial Number", "serial_number", required=True),
    Column("Voltage", "voltage"),
    Column("Power Source", "power_source"),
    Column("Last Maintenance Date", "last_maintenance_date"),
    Column("Next Maintenance Date", "next_maintenance_date"),
    Column("Location", "location"),
    Column("IP Address", "ip_address"),
    Column("Status", "status"),
    Column("Purchase Date", "purchase_date"),
    Column("Comment", "comment"),
    Column("Branch", "branch", source="branch.name", lookup=("assets.Branch", "name")),
]


class UPSLogSerializer(serializers.ModelSerializer):
    changed_by_username = serializers.CharField(
        source="changed_by.username", read_only=True
    )

    class Meta:
        model = UPSLog
        fields = (
            "id",
            "old_status",
            "new_status",
            "old_location",
            "new_location",
            "old_branch",
            "new_branch",
            "old_voltage",
            "new_voltage",
            "old_power_source",
            "new_power_source",
            "old_last_maintenance_date",
            "new_last_maintenance_date",
            "old_next_maintenance_date",
            "new_next_maintenance_date",
            "changed_by",
            "changed_by_username",
            "change_time",
            "comment",
        )
        read_only_fields = fields


class UPSSerializer(StockOnCreateMixin, serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    logs = UPSLogSerializer(many=True, read_only=True)

    class Meta:
        model = UPS
        fields = (
            "id",
            "model",
            "serial_number",
            "location",
            "ip_address",
            "status",
            "purchase_date",
            "voltage",
            "power_source",
            "last_maintenance_date",
            "next_maintenance_date",
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


class UPSViewSet(ExcelIOMixin, viewsets.ModelViewSet):
    queryset = UPS.objects.select_related("branch", "created_by").prefetch_related("logs")
    serializer_class = UPSSerializer
    search_fields = ["serial_number", "model", "ip_address", "location"]
    filterset_fields = ["status", "branch", "power_source"]
    ordering_fields = ["created_at", "serial_number", "next_maintenance_date", "status"]
    ordering = ["-created_at"]

    excel_columns = EXCEL_COLUMNS
    excel_sheet_name = "UPS Devices"

    ui_title = "UPS Devices"
    ui_group = "Infrastructure"
    ui_icon = "battery"
    ui_list_fields = [
        "serial_number",
        "model",
        "status",
        "power_source",
        "next_maintenance_date",
        "branch_name",
    ]
    ui_log_field = "logs"
