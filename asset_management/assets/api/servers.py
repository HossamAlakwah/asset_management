from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.models import Server, ServerLog

from .excel import Column, ExcelIOMixin
from .stock import RequireOnCreateMixin, StockOnCreateMixin

EXCEL_COLUMNS = [
    Column("Hostname", "hostname", required=True),
    Column("Model", "model", required=True),
    Column("Serial Number", "serial_number", required=True),
    Column("CPU Cores", "cpu_cores", required=True),
    Column("RAM GB", "ram_gb", required=True),
    Column("Storage GB", "storage_gb", required=True),
    Column("Hypervisor", "hypervisor", required=True),
    Column("Location", "location"),
    Column("IP Address", "ip_address", required=True),
    Column("MAC Address", "mac_address"),
    Column("Status", "status"),
    Column("Purchase Date", "purchase_date"),
    Column("Comment", "comment"),
    Column("Branch", "branch", source="branch.name", lookup=("assets.Branch", "name")),
]


class ServerLogSerializer(serializers.ModelSerializer):
    changed_by_username = serializers.CharField(
        source="changed_by.username", read_only=True
    )

    class Meta:
        model = ServerLog
        fields = (
            "id",
            "old_status",
            "new_status",
            "old_location",
            "new_location",
            "old_branch",
            "new_branch",
            "old_ip_address",
            "new_ip_address",
            "old_cpu",
            "new_cpu",
            "old_ram",
            "new_ram",
            "old_storage",
            "new_storage",
            "changed_by",
            "changed_by_username",
            "change_time",
            "comment",
        )
        read_only_fields = fields


class ServerSerializer(RequireOnCreateMixin, StockOnCreateMixin, serializers.ModelSerializer):
    require_on_create = ("ip_address",)
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    logs = ServerLogSerializer(many=True, read_only=True)

    class Meta:
        model = Server
        fields = (
            "id",
            "model",
            "serial_number",
            "hostname",
            "location",
            "ip_address",
            "mac_address",
            "status",
            "purchase_date",
            "cpu_cores",
            "ram_gb",
            "storage_gb",
            "hypervisor",
            "available_cpu_cores",
            "available_ram_gb",
            "available_storage_gb",
            "comment",
            "branch",
            "branch_name",
            "created_at",
            "updated_at",
            "created_by",
            "created_by_username",
            "logs",
        )
        read_only_fields = (
            "id",
            "available_cpu_cores",
            "available_ram_gb",
            "available_storage_gb",
            "created_at",
            "updated_at",
            "created_by",
        )

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


class ServerViewSet(ExcelIOMixin, viewsets.ModelViewSet):
    queryset = Server.objects.select_related("branch", "created_by").prefetch_related(
        "logs", "vms"
    )
    serializer_class = ServerSerializer
    search_fields = ["serial_number", "hostname", "ip_address", "model"]
    filterset_fields = ["status", "branch", "hypervisor"]
    ordering_fields = ["created_at", "hostname", "serial_number", "status"]
    ordering = ["-created_at"]

    excel_columns = EXCEL_COLUMNS
    excel_sheet_name = "Servers"

    ui_title = "Servers"
    ui_group = "Compute"
    ui_icon = "server"
    ui_list_fields = [
        "hostname",
        "serial_number",
        "status",
        "hypervisor",
        "available_cpu_cores",
        "available_ram_gb",
        "branch_name",
    ]
    ui_log_field = "logs"

    @action(detail=True, methods=["get"])
    def resources(self, request, pk=None):
        server = self.get_object()
        return Response(
            {
                "hostname": server.hostname,
                "cpu_cores": server.cpu_cores,
                "ram_gb": server.ram_gb,
                "storage_gb": server.storage_gb,
                "available_cpu_cores": server.available_cpu_cores,
                "available_ram_gb": server.available_ram_gb,
                "available_storage_gb": server.available_storage_gb,
            }
        )
