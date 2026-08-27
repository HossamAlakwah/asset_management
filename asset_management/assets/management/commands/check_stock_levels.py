from django.core.management.base import BaseCommand

from assets.models import NotificationConfig
from assets.utils.notifications import evaluate_config


class Command(BaseCommand):
    help = "Checks stock levels and sends notifications based on configured thresholds"

    def add_arguments(self, parser):
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Display detailed information about the checking process",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate the process without actually sending emails",
        )

    def handle(self, *args, **options):
        verbose = options["verbose"]
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write(self.style.NOTICE("DRY RUN: No emails will be sent"))

        notifications = NotificationConfig.objects.filter(is_active=True)
        if verbose:
            self.stdout.write(
                f"Found {notifications.count()} active notification configurations"
            )

        email_count = 0
        alert_count = 0

        for notification in notifications:
            if verbose:
                self.stdout.write(f"\nChecking: {notification}")
            try:
                result = evaluate_config(notification, send=not dry_run)
                if result.get("triggered"):
                    alert_count += 1
                    emailed = (
                        result.get("recipients", 0)
                        if dry_run
                        else result.get("emailed", 0)
                    )
                    email_count += emailed
                    if verbose:
                        self.stdout.write(
                            self.style.WARNING(
                                f"  LOW STOCK: {result.get('stock')} <= {result.get('threshold')}"
                            )
                        )
                elif verbose:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Stock OK: {result.get('stock')} > {result.get('threshold')}"
                        )
                    )
            except Exception as error:
                self.stdout.write(
                    self.style.ERROR(f"  Error checking {notification}: {error}")
                )

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("STOCK CHECK SUMMARY"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"Configurations checked: {notifications.count()}")
        self.stdout.write(f"Low stock alerts found: {alert_count}")
        self.stdout.write(
            f"Emails {'that would be ' if dry_run else ''}sent: {email_count}"
        )
        if dry_run:
            self.stdout.write(
                self.style.NOTICE("This was a dry run. No actual emails were sent.")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Stock level check completed."))
