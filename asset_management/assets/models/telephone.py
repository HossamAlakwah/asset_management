from django.conf import settings
from django.db import models
from django.utils import timezone

from assets.assignment import sync_assignment


class Telephone(models.Model):
    class Status(models.TextChoices):
        IN_USE = "In Use", "In Use"
        DAMAGE = "Damage", "Damage"
        STOCK = "Stock", "Stock"

    product = models.CharField(max_length=50)
    serial = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.STOCK, db_index=True
    )
    brand = models.CharField(max_length=50)
    employee = models.ForeignKey(
        "assets.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="telephones",
    )
    branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        related_name="telephones",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_telephones",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Telephone"
        verbose_name_plural = "Telephones"
        indexes = [
            models.Index(fields=["branch", "status"]),
        ]

    def save(self, *args, **kwargs):
        sync_assignment(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.serial}"


class TelephoneLog(models.Model):
    telephone = models.ForeignKey(
        Telephone, on_delete=models.CASCADE, related_name="logs"
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    old_employee = models.ForeignKey(
        "assets.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="telephone_old_employee_logs",
    )
    new_employee = models.ForeignKey(
        "assets.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="telephone_new_employee_logs",
    )
    branch = models.ForeignKey(
        "assets.Branch", on_delete=models.SET_NULL, null=True, blank=True
    )
    change_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-change_time"]
        verbose_name = "Telephone Log"
        verbose_name_plural = "Telephone Logs"

    def __str__(self):
        return f"Log for {self.telephone.serial} at {self.change_time}"
