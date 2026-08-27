from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("super_admin", "Super Admin"),
        ("admin", "Admin"),
        ("user", "User"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role in ("admin", "super_admin") or self.is_staff or self.is_superuser

    def is_super_admin(self):
        return self.role == "super_admin" or self.is_superuser

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username


class LoginLock(models.Model):
    """Failed sign-in counter keyed by IP or username."""

    KIND_IP = "ip"
    KIND_USERNAME = "username"
    KIND_CHOICES = (
        (KIND_IP, "IP"),
        (KIND_USERNAME, "Username"),
    )

    kind = models.CharField(max_length=16, choices=KIND_CHOICES)
    value = models.CharField(max_length=150)
    failures = models.PositiveIntegerField(default=0)
    window_started = models.DateTimeField()
    locked_until = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("kind", "value"), name="uniq_loginlock_kind_value"),
        ]

    def __str__(self):
        return f"{self.kind}:{self.value} ({self.failures})"


class TwoFactorDevice(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="totp_device",
    )
    secret = models.CharField(max_length=32)
    confirmed = models.BooleanField(default=False)
    backup_hashes = models.JSONField(default=list, blank=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        state = "on" if self.confirmed else "pending"
        return f"2FA {state} for {self.user.username}"
