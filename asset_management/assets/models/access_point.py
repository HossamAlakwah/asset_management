from django.conf import settings
from django.db import models
from django.utils import timezone


class AccessPoint(models.Model):
    class Status(models.TextChoices):
        STOCK = "Stock", "Stock"
        IN_USE = "In Use", "In Use"
        DAMAGE = "Damage", "Damage"

    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    ip_address = models.GenericIPAddressField(protocol="both", null=True, blank=True)
    mac_address = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.STOCK, db_index=True
    )
    purchase_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="access_points",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_access_points",
    )

    class Meta:
        verbose_name = "Access Point"
        verbose_name_plural = "Access Points"
        indexes = [
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["expiry_date"]),
        ]

    def __str__(self):
        return f"{self.model} - {self.serial_number}"


class AccessPointLog(models.Model):
    access_point = models.ForeignKey(
        AccessPoint, on_delete=models.CASCADE, related_name="logs"
    )
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    old_location = models.CharField(max_length=200, blank=True, null=True)
    new_location = models.CharField(max_length=200)
    old_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accesspointlog_old_branch",
    )
    new_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accesspointlog_new_branch",
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    change_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-change_time"]
        verbose_name = "Access Point Log"
        verbose_name_plural = "Access Point Logs"

    def __str__(self):
        return f"Log for Access Point {self.access_point.serial_number}"
