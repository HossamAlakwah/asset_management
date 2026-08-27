from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from users.twofactor import disable_two_factor, two_factor_is_confirmed

User = get_user_model()


class Command(BaseCommand):
    help = "Turn off two-factor authentication for a user who lost their authenticator."

    def add_arguments(self, parser):
        parser.add_argument("username")

    def handle(self, *args, **options):
        username = options["username"]
        user = User.objects.filter(username=username).first()
        if user is None:
            raise CommandError(f"No user named {username}.")
        if not two_factor_is_confirmed(user):
            self.stdout.write(f"{username} does not have 2FA enabled.")
            return
        disable_two_factor(user)
        self.stdout.write(self.style.SUCCESS(f"Disabled 2FA for {username}."))
