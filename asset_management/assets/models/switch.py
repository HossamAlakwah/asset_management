from django.conf import settings
from django.db import models
from django.utils import timezone


class Switch(models.Model):
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
    number_of_ports = models.PositiveIntegerField()
    number_of_poe_ports = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="switches",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_switches",
    )

    class Meta:
        verbose_name = "Switch"
        verbose_name_plural = "Switches"
        indexes = [
            models.Index(fields=["branch", "status"]),
        ]

    def __str__(self):
        return f"{self.model} - {self.serial_number}"


class SwitchLog(models.Model):
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, related_name="logs")
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    old_location = models.CharField(max_length=200, blank=True, null=True)
    new_location = models.CharField(max_length=200)
    old_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="switchlog_old_branch",
    )
    new_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="switchlog_new_branch",
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    change_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-change_time"]
        verbose_name = "Switch Log"
        verbose_name_plural = "Switch Logs"

    def __str__(self):
        return f"Log for Switch {self.switch.serial_number}"
