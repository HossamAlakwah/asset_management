import logging

from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail

from assets.models import NotificationConfig, NotificationRecipient, SentNotification

logger = logging.getLogger(__name__)


def stock_count_for(notification):
    model_class = apps.get_model("assets", notification.model_name)
    return model_class.objects.filter(status="Stock").count()


def render_message(notification, current_count, threshold):
    model_name = notification.get_model_name_display()
    if notification.notification_message:
        return notification.notification_message.format(
            model=model_name,
            count=current_count,
            threshold=threshold,
        )
    return (
        f"Low stock alert: {model_name} stock is now {current_count}, "
        f"which is at or below the threshold of {threshold}."
    )


def send_stock_notification(notification, current_count, threshold):
    """Email every subscriber for this rule. Returns how many messages were sent."""
    message = render_message(notification, current_count, threshold)
    model_name = notification.get_model_name_display()
    emailed = 0
    recipients = notification.subscribers.filter(is_active=True)
    for recipient in recipients:
        try:
            send_mail(
                subject=f"Low Stock Alert: {model_name}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            SentNotification.objects.create(
                config=notification,
                recipient=recipient,
                triggered_by=f"{model_name} stock count",
                message=message,
            )
            emailed += 1
        except Exception:
            logger.exception("Failed to email %s", recipient.email)
    return emailed


def evaluate_config(notification, send=True):
    """Check one rule. Optionally send mail if it is currently triggered."""
    if notification.condition_type != "stock_count":
        return {
            "triggered": False,
            "reason": "Only stock-count alerts are supported.",
            "emailed": 0,
        }
    count = stock_count_for(notification)
    try:
        threshold = int(str(notification.condition_value).strip())
    except (TypeError, ValueError):
        return {
            "triggered": False,
            "reason": "Threshold must be a whole number.",
            "emailed": 0,
        }
    triggered = count <= threshold
    emailed = 0
    if triggered and send:
        emailed = send_stock_notification(notification, count, threshold)
    return {
        "triggered": triggered,
        "stock": count,
        "threshold": threshold,
        "emailed": emailed,
        "recipients": notification.subscribers.filter(is_active=True).count(),
    }


def check_stock_levels():
    """Send low-stock alerts for every active notification rule."""
    for notification in NotificationConfig.objects.filter(is_active=True):
        try:
            evaluate_config(notification, send=True)
        except Exception:
            logger.exception("Failed checking notification %s", notification)
