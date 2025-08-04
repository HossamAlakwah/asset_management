from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import (
    NVR,
    Asset,
    AssetLog,
    Camera,
    CameraLog,
    Firewall,
    FirewallLog,
    NVRLog,
    Screen,
    ScreenLog,
    Switch,
    SwitchLog,
    Telephone,
    TelephoneLog,
)

'''
asset management signals
These signals are used to log changes to assets, such as creation, updates, and deletions
'''
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

'''Screen management signals
These signals are used to log changes to screens, such as creation, updates, and deletions
'''
@receiver(post_save, sender=Screen)
def log_screen_create(sender, instance, created, **kwargs):
    if not created:
        return

    ScreenLog.objects.create(
        screen=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=None,
        new_status=instance.status,
        old_employee=instance.employee,
        new_employee=instance.employee,
        branch=instance.branch,
        change_time=timezone.now()
    )

@receiver(pre_save, sender=Screen)
def log_screen_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # Let post_save handle creation

    try:
        old = Screen.objects.get(pk=instance.pk)
    except Screen.DoesNotExist:
        return

    changed = (
        old.status != instance.status or
        old.employee != instance.employee or
        old.branch != instance.branch
    )

    if changed:
        ScreenLog.objects.create(
            screen=instance,
            changed_by=getattr(instance, '_changed_by', None),
            old_status=old.status,
            new_status=instance.status,
            old_employee=old.employee,
            new_employee=instance.employee,
            branch=instance.branch,
            change_time=timezone.now()
        )

@receiver(pre_delete, sender=Screen)
def log_screen_delete(sender, instance, **kwargs):
    ScreenLog.objects.create(
        screen=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=instance.status,
        new_status='Deleted',
        old_employee=instance.employee,
        new_employee=None,
        branch=instance.branch,
        change_time=timezone.now()
    )

'''Telephone management signals
These signals are used to log changes to telephones, such as creation, updates, and deletions
'''
@receiver(post_save, sender=Telephone)
def log_telephone_create(sender, instance, created, **kwargs):
    if not created:
        return

    TelephoneLog.objects.create(
        telephone=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=None,
        new_status=instance.status,
        old_employee=instance.employee,
        new_employee=instance.employee,
        branch=instance.branch,
        change_time=timezone.now()
    )

@receiver(pre_save, sender=Telephone)
def log_telephone_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # Let post_save handle creation

    try:
        old = Telephone.objects.get(pk=instance.pk)
    except Telephone.DoesNotExist:
        return

    changed = (
        old.status != instance.status or
        old.employee != instance.employee or
        old.branch != instance.branch
    )

    if changed:
        TelephoneLog.objects.create(
            telephone=instance,
            changed_by=getattr(instance, '_changed_by', None),
            old_status=old.status,
            new_status=instance.status,
            old_employee=old.employee,
            new_employee=instance.employee,
            branch=instance.branch,
            change_time=timezone.now()
        )

@receiver(pre_delete, sender=Telephone)
def log_telephone_delete(sender, instance, **kwargs):
    TelephoneLog.objects.create(
        telephone=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=instance.status,
        new_status='Deleted',
        old_employee=instance.employee,
        new_employee=None,
        branch=instance.branch,
        change_time=timezone.now()
    )


''' Camera management signals
These signals are used to log changes to cameras, such as creation, updates, and deletions
'''


@receiver(post_save, sender=Camera)
def log_camera_create(sender, instance, created, **kwargs):
    if not created:
        return  # Only handle new camera creation here

    CameraLog.objects.create(
        camera=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=None,
        new_status=instance.status,
        old_location=None,
        new_location="stock",
        old_branch=None,
        new_branch=instance.branch,
        comment=instance.comment,
        change_time=timezone.now()
    )


@receiver(pre_save, sender=Camera)
def log_camera_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # Creation will be handled in post_save

    try:
        old = Camera.objects.get(pk=instance.pk)
    except Camera.DoesNotExist:
        return

    changed = (
        old.status != instance.status or
        old.location != instance.location or
        old.branch != instance.branch
    )

    if changed:
        CameraLog.objects.create(
            camera=instance,
            changed_by=getattr(instance, '_changed_by', None),
            old_status=old.status,
            new_status=instance.status,
            old_location=old.location,
            new_location=instance.location,
            old_branch=old.branch,
            new_branch=instance.branch,
            comment=instance.comment,
            change_time=timezone.now()
        )


@receiver(pre_delete, sender=Camera)
def log_camera_delete(sender, instance, **kwargs):
    CameraLog.objects.create(
        camera=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=instance.status,
        new_status='Deleted',
        old_location=instance.location,
        new_location='Deleted',
        old_branch=instance.branch,
        new_branch=None,
        comment=instance.comment,
        change_time=timezone.now()
    )

''' NVR management signals
These signals are used to log changes to NVRs, such as creation, updates, and deletions
'''

@receiver(post_save, sender=NVR)
def log_nvr_create(sender, instance, created, **kwargs):
    if not created:
        return  # Skip updates, only log creation

    NVRLog.objects.create(
        nvr=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=None,
        new_status=instance.status,
        old_location=None,
        new_location="stock",
        old_branch=None,
        new_branch=instance.branch,
        comment=instance.comment,
        change_time=timezone.now()
    )


@receiver(pre_save, sender=NVR)
def log_nvr_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if object is new (creation is handled in post_save)

    try:
        old = NVR.objects.get(pk=instance.pk)
    except NVR.DoesNotExist:
        return

    changed = (
        old.status != instance.status or
        old.location != instance.location or
        old.branch != instance.branch
    )

    if changed:
        NVRLog.objects.create(
            nvr=instance,
            changed_by=getattr(instance, '_changed_by', None),
            old_status=old.status,
            new_status=instance.status,
            old_location=old.location,
            new_location=instance.location,
            old_branch=old.branch,
            new_branch=instance.branch,
            comment=instance.comment,
            change_time=timezone.now()
        )


@receiver(pre_delete, sender=NVR)
def log_nvr_delete(sender, instance, **kwargs):
    NVRLog.objects.create(
        nvr=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=instance.status,
        new_status='Deleted',
        old_location=instance.location,
        new_location='Deleted',
        old_branch=instance.branch,
        new_branch=None,
        comment=instance.comment,
        change_time=timezone.now()
    )

''' Firewall management signals
These signals are used to log changes to Firewalls, such as creation, updates, and deletions
'''
@receiver(post_save, sender=Firewall)
def log_firewall_create(sender, instance, created, **kwargs):
    if created:
        FirewallLog.objects.create(
            firewall=instance,
            changed_by=getattr(instance, '_changed_by', None),
            old_status=None,
            new_status=instance.status,
            old_location=None,
            new_location="Stock",
            old_branch=None,
            new_branch=instance.branch,
            comment=instance.comment,
            change_time=timezone.now()
        )


@receiver(pre_save, sender=Firewall)
def log_firewall_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # New object, handled in post_save

    try:
        old = Firewall.objects.get(pk=instance.pk)
    except Firewall.DoesNotExist:
        return

    changed = (
        old.status != instance.status or
        old.location != instance.location or
        old.branch != instance.branch
    )

    if changed:
        FirewallLog.objects.create(
            firewall=instance,
            changed_by=getattr(instance, '_changed_by', None),
            old_status=old.status,
            new_status=instance.status,
            old_location=old.location,
            new_location=instance.location,
            old_branch=old.branch,
            new_branch=instance.branch,
            comment=instance.comment,
            change_time=timezone.now()
        )

''' Switches management signals
These signals are used to log changes to Switches, such as creation, updates, and deletions
'''
@receiver(post_save, sender=Switch)
def log_switch_create(sender, instance, created, **kwargs):
    if not created:
        return  # Only handle new switch creation here

    SwitchLog.objects.create(
        switch=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=None,
        new_status=instance.status,
        old_location=None,
        new_location="stock",
        old_branch=None,
        new_branch=instance.branch,
        comment=instance.comment,
        change_time=timezone.now()
    )


@receiver(pre_save, sender=Switch)
def log_switch_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # Creation will be handled in post_save

    try:
        old = Switch.objects.get(pk=instance.pk)
    except Switch.DoesNotExist:
        return

    changed = (
        old.status != instance.status or
        old.location != instance.location or
        old.branch != instance.branch
    )

    if changed:
        SwitchLog.objects.create(
            switch=instance,
            changed_by=getattr(instance, '_changed_by', None),
            old_status=old.status,
            new_status=instance.status,
            old_location=old.location,
            new_location=instance.location,
            old_branch=old.branch,
            new_branch=instance.branch,
            comment=instance.comment,
            change_time=timezone.now()
        )


@receiver(pre_delete, sender=Switch)
def log_switch_delete(sender, instance, **kwargs):
    SwitchLog.objects.create(
        switch=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=instance.status,
        new_status='Deleted',
        old_location=instance.location,
        new_location='Deleted',
        old_branch=instance.branch,
        new_branch=None,
        comment=instance.comment,
        change_time=timezone.now()
    )
