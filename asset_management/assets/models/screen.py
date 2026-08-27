from django.conf import settings
from django.db import models
from django.utils import timezone

from assets.assignment import sync_assignment


class Screen(models.Model):
    class Product(models.TextChoices):
        SCREEN = "Screen", "Screen"
        SCREEN_PC = "Screen-PC", "Screen-PC"

    class Status(models.TextChoices):
        IN_USE = "In Use", "In Use"
        DAMAGE = "Damage", "Damage"
        STOCK = "Stock", "Stock"

    product = models.CharField(max_length=50, choices=Product.choices)
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
        related_name="screens",
    )
    branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        related_name="screens",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_screens",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Screen"
        verbose_name_plural = "Screens"
        indexes = [
            models.Index(fields=["branch", "status"]),
        ]

    def save(self, *args, **kwargs):
        sync_assignment(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.serial}"


class ScreenLog(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="logs")
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
        related_name="screen_old_employee_logs",
    )
    new_employee = models.ForeignKey(
        "assets.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="screen_new_employee_logs",
    )
    branch = models.ForeignKey(
        "assets.Branch", on_delete=models.SET_NULL, null=True, blank=True
    )
    change_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-change_time"]
        verbose_name = "Screen Log"
        verbose_name_plural = "Screen Logs"

    def __str__(self):
        return f"Log for {self.screen.serial} at {self.change_time}"
