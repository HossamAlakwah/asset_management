from django.conf import settings
from django.db import models
from django.utils import timezone


class ColocationVM(models.Model):
    class Environment(models.TextChoices):
        UAT = "uat", "UAT"
        PROD = "prod", "Production"

    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(protocol="IPv4")
    vcpu = models.PositiveIntegerField()
    vram_gb = models.PositiveIntegerField()
    allocated_storage_gb = models.PositiveIntegerField(default=0)
    operating_system = models.CharField(max_length=100, default="Ubuntu Linux")
    environment = models.CharField(max_length=20, choices=Environment.choices)
    comments = models.TextField(blank=True, null=True)
    contract_start = models.DateField(null=True, blank=True)
    contract_end = models.DateField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_colocation_vms",
    )

    class Meta:
        verbose_name = "Colocation VM"
        verbose_name_plural = "Colocation VMs"
        ordering = ["environment", "name"]
        indexes = [
            models.Index(fields=["environment"]),
            models.Index(fields=["contract_end"]),
            models.Index(fields=["renewal_date"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.environment})"

    @property
    def is_active_contract(self):
        today = timezone.now().date()
        return self.contract_end is None or self.contract_end >= today

    @property
    def is_due_for_renewal(self):
        today = timezone.now().date()
        return bool(self.renewal_date and self.renewal_date <= today)
