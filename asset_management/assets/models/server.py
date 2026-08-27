from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Server(models.Model):
    class Status(models.TextChoices):
        STOCK = "Stock", "Stock"
        IN_USE = "In Use", "In Use"
        DAMAGE = "Damage", "Damage"

    class Hypervisor(models.TextChoices):
        VMWARE = "vmware", "VMware ESXi"
        HYPERV = "hyperv", "Hyper-V"

    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    hostname = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    ip_address = models.GenericIPAddressField(protocol="both", null=True, blank=True)
    mac_address = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.STOCK, db_index=True
    )
    purchase_date = models.DateField(blank=True, null=True)
    cpu_cores = models.PositiveIntegerField()
    ram_gb = models.PositiveIntegerField()
    storage_gb = models.PositiveIntegerField()
    hypervisor = models.CharField(max_length=20, choices=Hypervisor.choices)
    available_cpu_cores = models.PositiveIntegerField(default=0, editable=False)
    available_ram_gb = models.PositiveIntegerField(default=0, editable=False)
    available_storage_gb = models.PositiveIntegerField(default=0, editable=False)
    comment = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="servers",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_servers",
    )

    class Meta:
        verbose_name = "Server"
        verbose_name_plural = "Servers"
        indexes = [
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["hostname"]),
        ]

    def save(self, *args, **kwargs):
        creating = self.pk is None
        if creating:
            self.available_cpu_cores = self.cpu_cores
            self.available_ram_gb = self.ram_gb
            self.available_storage_gb = self.storage_gb
        super().save(*args, **kwargs)
        if not creating:
            # Total capacity may have changed, so free capacity must be rebased.
            self.update_available_resources()

    def update_available_resources(self):
        """Recompute free capacity from allocated VMs, in DB and on this instance."""
        totals = self.vms.aggregate(
            used_cpu=Sum("vcpu"),
            used_ram=Sum("vram_gb"),
            used_storage=Sum("storage_gb"),
        )
        self.available_cpu_cores = max(self.cpu_cores - (totals["used_cpu"] or 0), 0)
        self.available_ram_gb = max(self.ram_gb - (totals["used_ram"] or 0), 0)
        self.available_storage_gb = max(
            self.storage_gb - (totals["used_storage"] or 0), 0
        )
        Server.objects.filter(pk=self.pk).update(
            available_cpu_cores=self.available_cpu_cores,
            available_ram_gb=self.available_ram_gb,
            available_storage_gb=self.available_storage_gb,
        )

    def __str__(self):
        return f"{self.hostname} ({self.serial_number})"


class ServerLog(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="logs")
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20, blank=True, null=True)
    old_location = models.CharField(max_length=200, blank=True, null=True)
    new_location = models.CharField(max_length=200, blank=True, null=True)
    old_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="serverlog_old_branch",
    )
    new_branch = models.ForeignKey(
        "assets.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="serverlog_new_branch",
    )
    old_ip_address = models.GenericIPAddressField(null=True, blank=True)
    new_ip_address = models.GenericIPAddressField(null=True, blank=True)
    old_cpu = models.PositiveIntegerField(null=True, blank=True)
    new_cpu = models.PositiveIntegerField(null=True, blank=True)
    old_ram = models.PositiveIntegerField(null=True, blank=True)
    new_ram = models.PositiveIntegerField(null=True, blank=True)
    old_storage = models.PositiveIntegerField(null=True, blank=True)
    new_storage = models.PositiveIntegerField(null=True, blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    change_time = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-change_time"]
        verbose_name = "Server Log"
        verbose_name_plural = "Server Logs"

    def __str__(self):
        return f"Log for Server {self.server.hostname}"
