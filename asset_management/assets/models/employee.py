from django.conf import settings
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        related_name="employees",
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_employees",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        indexes = [
            models.Index(fields=["branch", "department"]),
        ]

    def __str__(self):
        return self.name
