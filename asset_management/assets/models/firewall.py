from django.conf import settings
from django.db import models
from django.utils import timezone


class Firewall(models.Model):
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
    firmware_version = models.CharField(max_length=255, blank=True, null=True)
    number_of_ports = models.IntegerField(blank=True, null=True)
    license_expiry_date = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="firewalls",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_firewalls",
    )

    class Meta:
        verbose_name = "Firewall"
        verbose_name_plural = "Firewalls"
        indexes = [
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["license_expiry_date"]),
        ]

    def __str__(self):
        return f"{self.model} - {self.serial_number}"


class FirewallLog(models.Model):
    firewall = models.ForeignKey(Firewall, on_delete=models.CASCADE, related_name="logs")
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    old_location = models.CharField(max_length=200, blank=True, null=True)
    new_location = models.CharField(max_length=200)
    old_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="firewalllog_old_branch",
    )
    new_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="firewalllog_new_branch",
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    change_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-change_time"]
        verbose_name = "Firewall Log"
        verbose_name_plural = "Firewall Logs"

    def __str__(self):
        return f"Log for Firewall {self.firewall.serial_number}"
