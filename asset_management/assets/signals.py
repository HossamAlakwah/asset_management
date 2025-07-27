from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Asset, AssetLog


@receiver(post_save, sender=Asset)
def log_asset_create(sender, instance, created, **kwargs):
    if not created:
        return  # Only handle creation here

    AssetLog.objects.create(
        asset=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=None,
        new_status=instance.status,
        old_employee=None,
        new_employee=instance.employee_name,
        on_hand_date=instance.on_hand_date,
        return_date=instance.return_date,
        branch=instance.branch,
        change_time=timezone.now()
    )


@receiver(pre_save, sender=Asset)
def log_asset_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # Let post_save handle creation

    try:
        old = Asset.objects.get(pk=instance.pk)
    except Asset.DoesNotExist:
        return

    changed = (
        old.status != instance.status or
        old.employee_name != instance.employee_name or
        old.on_hand_date != instance.on_hand_date or
        old.return_date != instance.return_date or
        old.branch != instance.branch
    )

    if changed:
        AssetLog.objects.create(
            asset=instance,
            changed_by=getattr(instance, '_changed_by', None),
            old_status=old.status,
            new_status=instance.status,
            old_employee=old.employee_name,
            new_employee=instance.employee_name,
            on_hand_date=instance.on_hand_date,
            return_date=instance.return_date,
            branch=instance.branch,
            change_time=timezone.now()
        )


@receiver(pre_delete, sender=Asset)
def log_asset_delete(sender, instance, **kwargs):
    AssetLog.objects.create(
        asset=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=instance.status,
        new_status='Deleted',
        old_employee=instance.employee_name,
        new_employee=None,
        on_hand_date=instance.on_hand_date,
        return_date=instance.return_date,
        branch=instance.branch,
        change_time=timezone.now()
    )
