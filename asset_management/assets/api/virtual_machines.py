from rest_framework import serializers, viewsets

from assets.models import VirtualMachine, VirtualMachineLog

from .excel import Column, ExcelIOMixin
from .stock import RequireOnCreateMixin

EXCEL_COLUMNS = [
    Column(
        "Server Hostname",
        "server",
        source="server.hostname",
        lookup=("assets.Server", "hostname"),
        required=True,
    ),
    Column("Name", "name", required=True),
    Column("vCPU", "vcpu", required=True),
    Column("vRAM GB", "vram_gb", required=True),
    Column("Storage GB", "storage_gb", required=True),
    Column("IP Address", "ip_address", required=True),
    Column("Operating System", "operating_system"),
    Column("Environment", "environment"),
    Column("Status", "status"),
    Column("Comment", "comment"),
]


class VirtualMachineLogSerializer(serializers.ModelSerializer):
    changed_by_username = serializers.CharField(
        source="changed_by.username", read_only=True
    )

    class Meta:
        model = VirtualMachineLog
        fields = (
            "id",
            "old_status",
            "new_status",
            "changed_by",
            "changed_by_username",
            "change_time",
            "comment",
        )
        read_only_fields = fields


class VirtualMachineSerializer(RequireOnCreateMixin, serializers.ModelSerializer):
    require_on_create = ("ip_address",)
    server_hostname = serializers.CharField(source="server.hostname", read_only=True)
    logs = VirtualMachineLogSerializer(many=True, read_only=True)

    class Meta:
        model = VirtualMachine
        fields = (
            "id",
            "server",
            "server_hostname",
            "name",
            "ip_address",
            "operating_system",
            "vcpu",
            "vram_gb",
            "storage_gb",
            "environment",
            "status",
            "comment",
            "created_at",
            "updated_at",
            "logs",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        view = self.context.get("view")
        if view and getattr(view, "action", None) != "retrieve":
            data.pop("logs", None)
        return data

    def validate(self, attrs):
        attrs = super().validate(attrs)

        def current(name, default=0):
            if name in attrs:
                return attrs[name]
            return getattr(self.instance, name, default)

        server = current("server", None)
        if server is None:
            return attrs

        probe = self.instance or VirtualMachine()
        probe.server = server
        available_cpu, available_ram, available_storage = probe.free_capacity_on(server)

        errors = {}
        if available_cpu < current("vcpu"):
            errors["vcpu"] = f"Only {available_cpu} vCPU free on {server.hostname}."
        if available_ram < current("vram_gb"):
            errors["vram_gb"] = f"Only {available_ram} GB RAM free on {server.hostname}."
        if available_storage < current("storage_gb"):
            errors["storage_gb"] = (
                f"Only {available_storage} GB storage free on {server.hostname}."
            )
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        vm = VirtualMachine(**validated_data)
        if request:
            vm._changed_by = request.user
        vm.save()
        return vm

    def update(self, instance, validated_data):
        request = self.context.get("request")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if request:
            instance._changed_by = request.user
        instance.save()
        return instance


class VirtualMachineViewSet(ExcelIOMixin, viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.select_related("server").prefetch_related("logs")
    serializer_class = VirtualMachineSerializer
    search_fields = ["name", "ip_address", "operating_system", "server__hostname"]
    filterset_fields = ["status", "environment", "server"]
    ordering_fields = ["created_at", "name", "status"]
    ordering = ["name"]

    excel_columns = EXCEL_COLUMNS
    excel_sheet_name = "Virtual Machines"

    ui_title = "Virtual Machines"
    ui_group = "Compute"
    ui_icon = "cube"
    ui_list_fields = [
        "name",
        "server_hostname",
        "status",
        "environment",
        "vcpu",
        "vram_gb",
        "storage_gb",
    ]
    ui_log_field = "logs"
