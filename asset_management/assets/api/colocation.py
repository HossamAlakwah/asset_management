from rest_framework import serializers, viewsets

from assets.models import ColocationVM

from .excel import Column, ExcelIOMixin

EXCEL_COLUMNS = [
    Column("Name", "name", required=True),
    Column("IP Address", "ip_address", required=True),
    Column("vCPU", "vcpu", required=True),
    Column("vRAM GB", "vram_gb", required=True),
    Column("Allocated Storage GB", "allocated_storage_gb"),
    Column("Operating System", "operating_system"),
    Column("Environment", "environment", required=True),
    Column("Contract Start", "contract_start"),
    Column("Contract End", "contract_end"),
    Column("Renewal Date", "renewal_date"),
    Column("Comments", "comments"),
]


class ColocationVMSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    is_active_contract = serializers.BooleanField(read_only=True)
    is_due_for_renewal = serializers.BooleanField(read_only=True)

    class Meta:
        model = ColocationVM
        fields = (
            "id",
            "name",
            "ip_address",
            "vcpu",
            "vram_gb",
            "allocated_storage_gb",
            "operating_system",
            "environment",
            "comments",
            "contract_start",
            "contract_end",
            "renewal_date",
            "is_active_contract",
            "is_due_for_renewal",
            "created_at",
            "updated_at",
            "created_by",
            "created_by_username",
        )
        read_only_fields = ("id", "created_at", "updated_at", "created_by")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        start = attrs.get(
            "contract_start",
            getattr(self.instance, "contract_start", None),
        )
        end = attrs.get(
            "contract_end",
            getattr(self.instance, "contract_end", None),
        )
        if start and end and end < start:
            raise serializers.ValidationError(
                {"contract_end": "Contract end date cannot be before the start date."}
            )
        return attrs


class ColocationVMViewSet(ExcelIOMixin, viewsets.ModelViewSet):
    queryset = ColocationVM.objects.select_related("created_by")
    serializer_class = ColocationVMSerializer
    search_fields = ["name", "ip_address", "operating_system"]
    filterset_fields = ["environment"]
    ordering_fields = ["name", "environment", "contract_end", "renewal_date"]
    ordering = ["environment", "name"]

    excel_columns = EXCEL_COLUMNS
    excel_sheet_name = "Colocation VMs"

    ui_title = "Colocation VMs"
    ui_group = "Compute"
    ui_icon = "cloud"
    ui_list_fields = [
        "name",
        "environment",
        "ip_address",
        "vcpu",
        "vram_gb",
        "contract_end",
        "is_active_contract",
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
