# management/commands/check_stock_levels.py
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from assets.models import NotificationConfig, NotificationRecipient, SentNotification


class Command(BaseCommand):
    help = 'Checks stock levels and sends notifications based on configured thresholds'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose', 
            action='store_true',
            help='Display detailed information about the checking process',
        )
        parser.add_argument(
            '--dry-run', 
            action='store_true',
            help='Simulate the process without actually sending emails',
        )
    
    def handle(self, *args, **options):
        verbose = options['verbose']
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.NOTICE("DRY RUN: No emails will be sent"))
        
        if verbose:
            self.stdout.write(self.style.NOTICE("Starting stock level check..."))
        
        # Get all active notification configurations
        notifications = NotificationConfig.objects.filter(is_active=True)
        
        if verbose:
            self.stdout.write(f"Found {notifications.count()} active notification configurations")
        
        email_count = 0
        alert_count = 0
        
        for notification in notifications:
            if verbose:
                self.stdout.write(f"\nChecking: {notification}")
            
            try:
                # Get the model class
                model_class = apps.get_model('assets', notification.model_name)
                
                if notification.condition_type == 'stock_count':
                    # Count items in stock for this model
                    in_stock_count = model_class.objects.filter(status='Stock').count()
                    threshold = int(notification.condition_value)
                    
                    if verbose:
                        self.stdout.write(f"  {notification.model_name} in stock: {in_stock_count}")
                        self.stdout.write(f"  Threshold: {threshold}")
                    
                    if in_stock_count <= threshold:
                        alert_count += 1
                        if verbose:
                            self.stdout.write(self.style.WARNING(
                                f"  ⚠️  LOW STOCK ALERT: {in_stock_count} <= {threshold}"
                            ))
                        
                        # Send notifications
                        recipients = NotificationRecipient.objects.filter(
                            is_active=True,
                            models_to_notify=notification
                        )
                        
                        if verbose:
                            self.stdout.write(f"  Notifying {recipients.count()} recipients")
                        
                        model_name = notification.get_model_name_display()
                        
                        # Prepare message
                        if notification.notification_message:
                            message = notification.notification_message.format(
                                model=model_name,
                                count=in_stock_count,
                                threshold=threshold
                            )
                        else:
                            message = f"Low stock alert: {model_name} stock is now {in_stock_count}, which is at or below the threshold of {threshold}."
                        
                        subject = f"Low Stock Alert: {model_name}"
                        
                        for recipient in recipients:
                            if verbose:
                                self.stdout.write(f"    📧 Preparing email for: {recipient.email}")
                                self.stdout.write(f"    Subject: {subject}")
                                self.stdout.write(f"    Message: {message[:100]}...")
                            
                            if not dry_run:
                                try:
                                    # Send actual email
                                    send_mail(
                                        subject=subject,
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
                                    
                                    if verbose:
                                        self.stdout.write(self.style.SUCCESS(
                                            f"    ✅ Email sent to {recipient.email}"
                                        ))
                                    email_count += 1
                                    
                                except Exception as e:
                                    self.stdout.write(self.style.ERROR(
                                        f"    ❌ Failed to send email to {recipient.email}: {e}"
                                    ))
                            else:
                                if verbose:
                                    self.stdout.write(self.style.NOTICE(
                                        f"    📝 [DRY RUN] Would send email to {recipient.email}"
                                    ))
                                email_count += 1  # Count even in dry run for reporting
                    else:
                        if verbose:
                            self.stdout.write(self.style.SUCCESS(
                                f"  ✅ Stock level OK: {in_stock_count} > {threshold}"
                            ))
            
            except LookupError:
                self.stdout.write(self.style.ERROR(
                    f"  ❌ Model '{notification.model_name}' not found"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"  ❌ Error checking {notification}: {e}"
                ))
        
        # Summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS("STOCK CHECK SUMMARY"))
        self.stdout.write("="*50)
        self.stdout.write(f"Configurations checked: {notifications.count()}")
        self.stdout.write(f"Low stock alerts found: {alert_count}")
        self.stdout.write(f"Emails {'that would be ' if dry_run else ''}sent: {email_count}")
        
        if dry_run:
            self.stdout.write(self.style.NOTICE(
                "This was a dry run. No actual emails were sent."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                "✅ Stock level check completed successfully"
            ))