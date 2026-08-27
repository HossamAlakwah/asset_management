from django.conf import settings
from django.db import models
from django.utils import timezone


class UPS(models.Model):
    class Status(models.TextChoices):
        STOCK = "Stock", "Stock"
        IN_USE = "In Use", "In Use"
        DAMAGE = "Damage", "Damage"

    class PowerSource(models.TextChoices):
        UTILITY = "Utility", "Utility"
        BATTERY = "Battery", "Battery"
        GENERATOR = "Generator", "Generator"

    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    ip_address = models.GenericIPAddressField(protocol="both", null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.STOCK, db_index=True
    )
    purchase_date = models.DateField(blank=True, null=True)
    voltage = models.FloatField(blank=True, null=True)
    power_source = models.CharField(
        max_length=20, choices=PowerSource.choices, blank=True, null=True
    )
    last_maintenance_date = models.DateField(blank=True, null=True)
    next_maintenance_date = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ups_devices",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_ups_devices",
    )

    class Meta:
        verbose_name = "UPS"
        verbose_name_plural = "UPS Devices"
        indexes = [
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["next_maintenance_date"]),
        ]

    def __str__(self):
        return f"{self.model} - {self.serial_number}"


class UPSLog(models.Model):
    ups = models.ForeignKey(UPS, on_delete=models.CASCADE, related_name="logs")
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    old_location = models.CharField(max_length=200, blank=True, null=True)
    new_location = models.CharField(max_length=200)
    old_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="upslog_old_branch",
    )
    new_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="upslog_new_branch",
    )
    old_voltage = models.FloatField(blank=True, null=True)
    new_voltage = models.FloatField(blank=True, null=True)
    old_power_source = models.CharField(
        max_length=20, choices=UPS.PowerSource.choices, blank=True, null=True
    )
    new_power_source = models.CharField(
        max_length=20, choices=UPS.PowerSource.choices, blank=True, null=True
    )
    old_last_maintenance_date = models.DateField(blank=True, null=True)
    new_last_maintenance_date = models.DateField(blank=True, null=True)
    old_next_maintenance_date = models.DateField(blank=True, null=True)
    new_next_maintenance_date = models.DateField(blank=True, null=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    change_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-change_time"]
        verbose_name = "UPS Log"
        verbose_name_plural = "UPS Logs"

    def __str__(self):
        return f"Log for UPS {self.ups.serial_number}"
