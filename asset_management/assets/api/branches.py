from rest_framework import serializers, viewsets

from assets.models import Branch

from .excel import Column, ExcelIOMixin

EXCEL_COLUMNS = [
    Column("Name", "name", required=True),
    Column("Selectable", "choosable"),
]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ("id", "name", "slug", "choosable", "created_at")
        read_only_fields = ("id", "slug", "created_at")


class BranchViewSet(ExcelIOMixin, viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    search_fields = ["name", "slug"]
    filterset_fields = ["choosable"]
    ordering_fields = ["name", "created_at"]

    excel_columns = EXCEL_COLUMNS
    excel_sheet_name = "Branches"

    ui_title = "Branches"
    ui_group = "Organisation"
    ui_icon = "building"
    ui_list_fields = ["name", "slug", "choosable", "created_at"]
