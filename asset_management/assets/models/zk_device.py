from django.conf import settings
from django.db import models
from django.utils import timezone


class ZKDevice(models.Model):
    class Status(models.TextChoices):
        STOCK = "Stock", "Stock"
        IN_USE = "In Use", "In Use"
        DAMAGE = "Damage", "Damage"

    class DeviceType(models.TextChoices):
        ATTENDANCE = "Attendance Machine", "Attendance Machine"
        ACCESS_CONTROL = "Access Control", "Access Control"
        ACCESS_DOOR = "Access Door", "Access Door"

    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    ip_address = models.GenericIPAddressField(protocol="both")
    mac_address = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.STOCK, db_index=True
    )
    purchase_date = models.DateField(blank=True, null=True)
    device_type = models.CharField(max_length=50, choices=DeviceType.choices)
    vendor = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="zk_devices",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_zk_devices",
    )

    class Meta:
        verbose_name = "ZK Device"
        verbose_name_plural = "ZK Devices"
        indexes = [
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["device_type"]),
            models.Index(fields=["ip_address"]),
        ]

    def __str__(self):
        return f"{self.device_type} - {self.serial_number} ({self.ip_address})"


class ZKDeviceLog(models.Model):
    device = models.ForeignKey(ZKDevice, on_delete=models.CASCADE, related_name="logs")
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    old_location = models.CharField(max_length=200, blank=True, null=True)
    new_location = models.CharField(max_length=200)
    old_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="zkdevicelog_old_branch",
    )
    new_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="zkdevicelog_new_branch",
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    change_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-change_time"]
        verbose_name = "ZK Device Log"
        verbose_name_plural = "ZK Device Logs"

    def __str__(self):
        return f"Log for {self.device.serial_number}"
