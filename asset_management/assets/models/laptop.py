from django.conf import settings
from django.db import models
from django.utils import timezone

from assets.assignment import sync_assignment


class Laptop(models.Model):
    class Status(models.TextChoices):
        IN_USE = "In Use", "In Use"
        STOCK = "Stock", "Stock"
        DAMAGE = "Damage", "Damage"

    class Cpu(models.TextChoices):
        I3 = "i3", "Intel Core i3"
        I5 = "i5", "Intel Core i5"
        I7 = "i7", "Intel Core i7"
        I9 = "i9", "Intel Core i9"

    class CpuGeneration(models.TextChoices):
        GEN_1 = "1", "1st Gen"
        GEN_2 = "2", "2nd Gen"
        GEN_3 = "3", "3rd Gen"
        GEN_4 = "4", "4th Gen"
        GEN_5 = "5", "5th Gen"
        GEN_6 = "6", "6th Gen"
        GEN_7 = "7", "7th Gen"
        GEN_8 = "8", "8th Gen"
        GEN_9 = "9", "9th Gen"
        GEN_10 = "10", "10th Gen"
        GEN_11 = "11", "11th Gen"
        GEN_12 = "12", "12th Gen"
        GEN_13 = "13", "13th Gen"

    class Ram(models.TextChoices):
        GB_4 = "4GB", "4 GB"
        GB_8 = "8GB", "8 GB"
        GB_16 = "16GB", "16 GB"
        GB_32 = "32GB", "32 GB"

    product = models.CharField(max_length=255)
    serial = models.CharField(max_length=255, unique=True)
    cpu = models.CharField(max_length=20, choices=Cpu.choices, blank=True, null=True)
    cpu_generation = models.CharField(
        max_length=3, choices=CpuGeneration.choices, blank=True, null=True
    )
    ram = models.CharField(max_length=10, choices=Ram.choices, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.STOCK, db_index=True
    )
    employee = models.ForeignKey(
        "assets.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="laptops",
    )
    warranty = models.DateField(blank=True, null=True)
    on_hand_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        related_name="laptops",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_laptops",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Laptop"
        verbose_name_plural = "Laptops"
        indexes = [
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["employee", "status"]),
        ]

    def save(self, *args, **kwargs):
        sync_assignment(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.serial}"


class LaptopStorage(models.Model):
    class StorageType(models.TextChoices):
        HDD = "HDD", "HDD"
        SSD = "SSD", "SSD"

    class StorageSize(models.TextChoices):
        GB_128 = "128", "128 GB"
        GB_256 = "256", "256 GB"
        GB_512 = "512", "512 GB"
        TB_1 = "1TB", "1 TB"

    laptop = models.ForeignKey(
        Laptop, on_delete=models.CASCADE, related_name="storage_devices"
    )
    type = models.CharField(max_length=10, choices=StorageType.choices)
    size = models.CharField(max_length=10, choices=StorageSize.choices)

    def __str__(self):
        return f"{self.size} {self.type}"


class LaptopLog(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, related_name="logs")
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
        related_name="laptop_old_employee_logs",
    )
    new_employee = models.ForeignKey(
        "assets.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="laptop_new_employee_logs",
    )
    on_hand_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    branch = models.ForeignKey(
        "assets.Branch", on_delete=models.SET_NULL, null=True, blank=True
    )
    change_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-change_time"]
        verbose_name = "Laptop Log"
        verbose_name_plural = "Laptop Logs"

    def __str__(self):
        return f"Log for {self.laptop.serial} at {self.change_time}"
