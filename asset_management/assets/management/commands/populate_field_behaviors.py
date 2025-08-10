from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models

from assets.models import FieldBehavior


class Command(BaseCommand):
    help = "Populate FieldBehavior with all model fields"

    def handle(self, *args, **kwargs):
        model_classes = [
            'UPS', 'Asset', 'Camera', 'Switch', 'Router',
            'AccessPoint', 'Firewall', 'Screen', 'Telephone', 'NVR'
        ]

        added = 0
        for model_name in model_classes:
            try:
                model = apps.get_model('assets', model_name)
            except LookupError:
                self.stdout.write(self.style.WARNING(f"Model not found: {model_name}"))
                continue

            for field in model._meta.get_fields():
                if field.auto_created:
                    continue

                # Allow ForeignKey fields like 'branch'
                if field.is_relation and not isinstance(field, models.ForeignKey):
                    continue

                field_name = field.name
                obj, created = FieldBehavior.objects.get_or_create(
                    model_name=model_name,
                    field_name=field_name,
                    defaults={'is_required': False, 'is_disabled': False}
                )
                if created:
                    added += 1

        self.stdout.write(self.style.SUCCESS(f"FieldBehavior populated. {added} new records added."))
