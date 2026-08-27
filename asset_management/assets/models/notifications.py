from django.db import models


class NotificationConfig(models.Model):
    MODEL_CHOICES = [
        ("Laptop", "Laptop"),
        ("Desktop", "Desktop"),
        ("Screen", "Screen"),
        ("Telephone", "Telephone"),
        ("Camera", "Camera"),
        ("NVR", "NVR"),
        ("Firewall", "Firewall"),
        ("Switch", "Switch"),
        ("AccessPoint", "Access Point"),
        ("Router", "Router"),
        ("UPS", "UPS"),
        ("ZKDevice", "ZK Device"),
        ("Server", "Server"),
    ]

    model_name = models.CharField(max_length=50, choices=MODEL_CHOICES)
    condition_type = models.CharField(
        max_length=20,
        choices=[("stock_count", "Stock Count")],
    )
    condition_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    notification_message = models.TextField(blank=True)

    class Meta:
        unique_together = ("model_name", "condition_type", "condition_value")

    def __str__(self):
        return f"{self.model_name} - {self.condition_type} - {self.condition_value}"


class NotificationRecipient(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    models_to_notify = models.ManyToManyField(
        NotificationConfig, blank=True, related_name="subscribers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class SentNotification(models.Model):
    config = models.ForeignKey(NotificationConfig, on_delete=models.CASCADE)
    recipient = models.ForeignKey(NotificationRecipient, on_delete=models.CASCADE)
    triggered_by = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sent_at"]
