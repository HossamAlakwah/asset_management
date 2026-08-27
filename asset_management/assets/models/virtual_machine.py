from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class VirtualMachine(models.Model):
    class Environment(models.TextChoices):
        UAT = "uat", "UAT"
        PROD = "prod", "Production"
        DEV = "dev", "Development"
        TEST = "test", "Testing"

    class Status(models.TextChoices):
        RUNNING = "running", "Running"
        STOPPED = "stopped", "Stopped"

    server = models.ForeignKey(
        "assets.Server", on_delete=models.CASCADE, related_name="vms"
    )
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(protocol="IPv4", blank=True, null=True)
    operating_system = models.CharField(max_length=100, default="Linux")
    vcpu = models.PositiveIntegerField()
    vram_gb = models.PositiveIntegerField()
    storage_gb = models.PositiveIntegerField()
    environment = models.CharField(
        max_length=20, choices=Environment.choices, default=Environment.PROD
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.RUNNING, db_index=True
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("server", "name")
        ordering = ["server", "name"]
        verbose_name = "Virtual Machine"
        verbose_name_plural = "Virtual Machines"
        indexes = [
            models.Index(fields=["server", "status"]),
            models.Index(fields=["environment"]),
        ]

    def free_capacity_on(self, server):
        """Capacity available to this VM, adding back what it already holds."""
        cpu = server.available_cpu_cores
        ram = server.available_ram_gb
        storage = server.available_storage_gb
        if self.pk and self.server_id == server.pk:
            previous = VirtualMachine.objects.filter(pk=self.pk).first()
            if previous:
                cpu += previous.vcpu
                ram += previous.vram_gb
                storage += previous.storage_gb
        return cpu, ram, storage

    def clean(self):
        if not self.server_id:
            return
        cpu, ram, storage = self.free_capacity_on(self.server)
        errors = {}
        if cpu < self.vcpu:
            errors["vcpu"] = f"Only {cpu} vCPU available on {self.server.hostname}."
        if ram < self.vram_gb:
            errors["vram_gb"] = f"Only {ram} GB RAM available on {self.server.hostname}."
        if storage < self.storage_gb:
            errors["storage_gb"] = (
                f"Only {storage} GB storage available on {self.server.hostname}."
            )
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.name} ({self.environment}) on {self.server.hostname}"


class VirtualMachineLog(models.Model):
    vm = models.ForeignKey(
        VirtualMachine, on_delete=models.CASCADE, related_name="logs"
    )
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    change_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-change_time"]
        verbose_name = "Virtual Machine Log"
        verbose_name_plural = "Virtual Machine Logs"

    def __str__(self):
        return f"Log for VM {self.vm.name}"
