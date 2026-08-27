from rest_framework import serializers, viewsets

from assets.models import Employee

from .excel import Column, ExcelIOMixin

EXCEL_COLUMNS = [
    Column("Name", "name", required=True),
    Column("Email", "email", required=True),
    Column("Department", "department", required=True),
    Column("Title", "title", required=True),
    Column("Branch", "branch", source="branch.name", lookup=("assets.Branch", "name")),
]


class EmployeeSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )

    class Meta:
        model = Employee
        fields = (
            "id",
            "name",
            "department",
            "title",
            "email",
            "branch",
            "branch_name",
            "creation_date",
            "created_by",
            "created_by_username",
        )
        read_only_fields = ("id", "creation_date", "created_by")


class EmployeeViewSet(ExcelIOMixin, viewsets.ModelViewSet):
    queryset = Employee.objects.select_related("branch", "created_by")
    serializer_class = EmployeeSerializer
    search_fields = ["name", "email", "department", "title"]
    filterset_fields = ["branch", "department"]
    ordering_fields = ["name", "creation_date", "department"]

    excel_columns = EXCEL_COLUMNS
    excel_sheet_name = "Employees"

    ui_title = "Employees"
    ui_group = "Organisation"
    ui_icon = "users"
    ui_list_fields = ["name", "email", "department", "title", "branch_name"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
