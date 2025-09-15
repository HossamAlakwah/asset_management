from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail

from assets.models import NotificationConfig


def check_stock_levels():
    """
    Check all configured stock levels and send notifications if needed
    """
    # Get all active notification configurations
    notifications = NotificationConfig.objects.filter(is_active=True)
    
    for notification in notifications:
        try:
            # Get the model class
            model_class = apps.get_model('assets', notification.model_name)
            
            if notification.condition_type == 'stock_count':
                # Count items in stock for this model
                in_stock_count = model_class.objects.filter(status='Stock').count()
                threshold = int(notification.condition_value)
                print(in_stock_count)
                print(threshold)
                if in_stock_count <= threshold:
                    send_stock_notification(notification, in_stock_count, threshold)
            
        except Exception as e:
            # Log error but don't break the entire process
            print(f"Error checking notification {notification}: {e}")
            # You might want to add proper logging here


def send_stock_notification(notification, current_count, threshold):
    """
    Send notification for low stock
    """
    from assets.models import NotificationRecipient, SentNotification
    
    model_name = notification.get_model_name_display()
    
    # Prepare message
    if notification.notification_message:
        message = notification.notification_message.format(
            model=model_name,
            count=current_count,
            threshold=threshold
        )
    else:
        message = f"Low stock alert: {model_name} stock is now {current_count}, which is at or below the threshold of {threshold}."
    
    # Get recipients for this notification
    recipients = NotificationRecipient.objects.filter(
        is_active=True,
        models_to_notify=notification
    )
    
    # Send emails
    for recipient in recipients:
        try:
            send_mail(
                subject=f"Low Stock Alert: {model_name}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            
            # Record that we sent this notification
            SentNotification.objects.create(
                config=notification,
                recipient=recipient,
                triggered_by=f"{model_name} stock count",
                message=message
            )
            print(f"Sent notification to {recipient.email} about {model_name}")
            
        except Exception as e:
            print(f"Failed to send email to {recipient.email}: {e}")