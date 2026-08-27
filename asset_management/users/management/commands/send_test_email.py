from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Send a test message through the configured email backend."

    def add_arguments(self, parser):
        parser.add_argument("to", help="Recipient email address")

    def handle(self, *args, **options):
        recipient = options["to"]
        self.stdout.write(f"Backend: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"Host: {settings.EMAIL_HOST or '(none)'}")
        self.stdout.write(f"From: {settings.DEFAULT_FROM_EMAIL}")
        try:
            sent = send_mail(
                subject="Asset Control test email",
                message=(
                    "This is a test from Asset Control. Password reset and "
                    "stock alerts use this same mail backend."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception as error:
            raise CommandError(f"Send failed: {error}") from error
        self.stdout.write(self.style.SUCCESS(f"Sent {sent} message(s) to {recipient}."))
