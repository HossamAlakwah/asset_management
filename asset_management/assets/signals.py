from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import (
    NVR,
    UPS,
    AccessPoint,
    AccessPointLog,
    Asset,
    AssetLog,
    Camera,
    CameraLog,
    Firewall,
    FirewallLog,
    NVRLog,
    Router,
    RouterLog,
    Screen,
    ScreenLog,
    Switch,
    SwitchLog,
    Telephone,
    TelephoneLog,
    UPSLog,
    ZKDevice,
    ZKDeviceLog,
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

''' access point signals
These signals are used to log changes to Switches, such as creation, updates, and deletions
'''
@receiver(post_save, sender=AccessPoint)
def log_access_point_create(sender, instance, created, **kwargs):
    if not created:
        return

    AccessPointLog.objects.create(
        access_point=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=None,
        new_status=instance.status,
        old_location=None,
        new_location='stock',
        old_branch=None,
        new_branch=instance.branch,
        comment=instance.comment,
        change_time=timezone.now()
    )


@receiver(pre_save, sender=AccessPoint)
def log_access_point_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = AccessPoint.objects.get(pk=instance.pk)
    except AccessPoint.DoesNotExist:
        return

    changed = (
        old.status != instance.status or
        old.location != instance.location or
        old.branch != instance.branch
    )

    if changed:
        AccessPointLog.objects.create(
            access_point=instance,
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


@receiver(pre_delete, sender=AccessPoint)
def log_access_point_delete(sender, instance, **kwargs):
    AccessPointLog.objects.create(
        access_point=instance,
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
    
''' router signals
These signals are used to log changes to Switches, such as creation, updates, and deletions
'''
@receiver(post_save, sender=Router)
def log_router_create(sender, instance, created, **kwargs):
    if not created:
        return

    RouterLog.objects.create(
        router=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=None,
        new_status=instance.status,
        old_location=None,
        new_location='stock',
        old_branch=None,
        new_branch=instance.branch,
        comment=instance.comment,
        change_time=timezone.now()
    )


@receiver(pre_save, sender=Router)
def log_router_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Router.objects.get(pk=instance.pk)
    except Router.DoesNotExist:
        return

    changed = (
        old.status != instance.status or
        old.location != instance.location or
        old.branch != instance.branch
    )

    if changed:
        RouterLog.objects.create(
            router=instance,
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


@receiver(pre_delete, sender=Router)
def log_router_delete(sender, instance, **kwargs):
    RouterLog.objects.create(
        router=instance,
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
    

'''
UPS part
'''
@receiver(post_save, sender=UPS)
def log_ups_create(sender, instance, created, **kwargs):
    if not created:
        return

    UPSLog.objects.create(
        ups=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=None,
        new_status=instance.status,
        old_location=None,
        new_location='stock',
        old_branch=None,
        new_branch=instance.branch,
        old_voltage=None,
        new_voltage=instance.voltage,
        old_power_source=None,
        new_power_source=instance.power_source,
        old_last_maintenance_date=None,
        new_last_maintenance_date=instance.last_maintenance_date,
        old_next_maintenance_date=None,
        new_next_maintenance_date=instance.next_maintenance_date,
        comment=instance.comment,
        change_time=timezone.now()
    )

@receiver(pre_save, sender=UPS)
def log_ups_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # skip if not yet saved

    try:
        old = UPS.objects.get(pk=instance.pk)
    except UPS.DoesNotExist:
        return

    changed = any([
        old.status != instance.status,
        old.location != instance.location,
        old.branch != instance.branch,
        old.voltage != instance.voltage,
        old.power_source != instance.power_source,
        old.last_maintenance_date != instance.last_maintenance_date,
        old.next_maintenance_date != instance.next_maintenance_date,
    ])

    if changed:
        UPSLog.objects.create(
            ups=instance,
            changed_by=getattr(instance, '_changed_by', None),
            old_status=old.status,
            new_status=instance.status,
            old_location=old.location,
            new_location=instance.location,
            old_branch=old.branch,
            new_branch=instance.branch,
            old_voltage=old.voltage,
            new_voltage=instance.voltage,
            old_power_source=old.power_source,
            new_power_source=instance.power_source,
            old_last_maintenance_date=old.last_maintenance_date,
            new_last_maintenance_date=instance.last_maintenance_date,
            old_next_maintenance_date=old.next_maintenance_date,
            new_next_maintenance_date=instance.next_maintenance_date,
            comment=instance.comment,
            change_time=timezone.now()
        )


@receiver(pre_delete, sender=UPS)
def log_ups_delete(sender, instance, **kwargs):
    UPSLog.objects.create(
        ups=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=instance.status,
        new_status='Deleted',
        old_location=instance.location,
        new_location='Deleted',
        old_branch=instance.branch,
        new_branch=None,
        old_voltage=instance.voltage,
        new_voltage=None,
        old_power_source=instance.power_source,
        new_power_source='Deleted',
        old_last_maintenance_date=instance.last_maintenance_date,
        new_last_maintenance_date=None,
        old_next_maintenance_date=instance.next_maintenance_date,
        new_next_maintenance_date=None,
        comment="Deleted",
        change_time=timezone.now()
    )



'''
ZKDevice signals
These signals are used to log changes to ZK Devices 
(Attendance Machine, Access Control, Access Door).
'''


@receiver(post_save, sender=ZKDevice)
def log_zkdevice_create(sender, instance, created, **kwargs):
    if not created:
        return

    ZKDeviceLog.objects.create(
        device=instance,
        changed_by=getattr(instance, '_changed_by', None),
        old_status=None,
        new_status=instance.status,
        old_location=None,
        new_location=instance.location or "Stock",
        old_branch=None,
        new_branch=instance.branch,
        comment=instance.comment,
        change_time=timezone.now()
    )


@receiver(pre_save, sender=ZKDevice)
def log_zkdevice_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = ZKDevice.objects.get(pk=instance.pk)
    except ZKDevice.DoesNotExist:
        return

    changed = (
        old.status != instance.status or
        old.location != instance.location or
        old.branch != instance.branch
    )

    if changed:
        ZKDeviceLog.objects.create(
            device=instance,
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


@receiver(pre_delete, sender=ZKDevice)
def log_zkdevice_delete(sender, instance, **kwargs):
    ZKDeviceLog.objects.create(
        device=instance,
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

from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Server, ServerLog, VirtualMachine, VirtualMachineLog


def update_server_resources(server: Server):
    """Recalculate server available resources based on VMs."""
    allocated_cpu = sum(vm.vcpu for vm in server.vms.all())
    allocated_ram = sum(vm.vram_gb for vm in server.vms.all())
    allocated_storage = sum(vm.storage_gb for vm in server.vms.all())

    server.available_cpu_cores = max(server.cpu_cores - allocated_cpu, 0)
    server.available_ram_gb = max(server.ram_gb - allocated_ram, 0)
    server.available_storage_gb = max(server.storage_gb - allocated_storage, 0)
    server.save(update_fields=["available_cpu_cores", "available_ram_gb", "available_storage_gb"])


"""
🔹 VirtualMachine signals
"""
@receiver(pre_save, sender=VirtualMachine)
def log_vm_changes(sender, instance, **kwargs):
    if instance.pk:  # Updating existing VM
        old_vm = VirtualMachine.objects.get(pk=instance.pk)
        changes = {}

        if old_vm.status != instance.status:
            changes["old_status"] = old_vm.status
            changes["new_status"] = instance.status

        if old_vm.vcpu != instance.vcpu or old_vm.vram_gb != instance.vram_gb or old_vm.storage_gb != instance.storage_gb:
            changes["comment"] = f"Resources updated (CPU {old_vm.vcpu}->{instance.vcpu}, RAM {old_vm.vram_gb}->{instance.vram_gb}, Storage {old_vm.storage_gb}->{instance.storage_gb})"

        if changes:
            VirtualMachineLog.objects.create(
                vm=instance,
                old_status=changes.get("old_status"),
                new_status=changes.get("new_status", instance.status),
                change_time=timezone.now(),
                comment=changes.get("comment"),
            )


@receiver(post_save, sender=VirtualMachine)
def update_server_on_vm_save(sender, instance, created, **kwargs):
    update_server_resources(instance.server)
    if created:
        VirtualMachineLog.objects.create(
            vm=instance,
            old_status=None,
            new_status=instance.status,
            change_time=timezone.now(),
            comment="VM created",
        )


@receiver(post_delete, sender=VirtualMachine)
def update_server_on_vm_delete(sender, instance, **kwargs):
    update_server_resources(instance.server)
    VirtualMachineLog.objects.create(
        vm=instance,
        old_status=instance.status,
        new_status="deleted",
        change_time=timezone.now(),
        comment="VM deleted",
    )


"""
🔹 Server signals
"""

@receiver(pre_save, sender=Server)
def log_server_changes(sender, instance, **kwargs):
    TRACK_FIELDS = ['ip_address', 'cpu_cores', 'ram_gb', 'storage_gb']

    if not instance.pk:
        return  # Skip creation, handled in post_save if needed

    try:
        old_server = Server.objects.get(pk=instance.pk)
    except Server.DoesNotExist:
        return

    changes = {}
    for field in TRACK_FIELDS:
        old_value = getattr(old_server, field)
        new_value = getattr(instance, field)
        if old_value != new_value:
            changes[field] = (old_value, new_value)

    if changes:
        ServerLog.objects.create(
            server=instance,
            change_time=timezone.now(),
            old_ip_address=changes.get('ip_address', (None, None))[0],
            new_ip_address=changes.get('ip_address', (None, None))[1],
            old_cpu=changes.get('cpu_cores', (None, None))[0],
            new_cpu=changes.get('cpu_cores', (None, None))[1],
            old_ram=changes.get('ram_gb', (None, None))[0],
            new_ram=changes.get('ram_gb', (None, None))[1],
            old_storage=changes.get('storage_gb', (None, None))[0],
            new_storage=changes.get('storage_gb', (None, None))[1],
            changed_by=getattr(instance, "_changed_by", None),
            comment="; ".join([f"{k} {v[0]}->{v[1]}" for k, v in changes.items()])
        )

@receiver(post_save, sender=VirtualMachine)
def update_server_resources_on_save(sender, instance, **kwargs):
    """Update server resources after a VM is created or updated"""
    if instance.server:
        instance.server.update_available_resources()

@receiver(post_delete, sender=VirtualMachine)
def update_server_resources_on_delete(sender, instance, **kwargs):
    """Update server resources after a VM is deleted"""
    if instance.server:
        instance.server.update_available_resources()