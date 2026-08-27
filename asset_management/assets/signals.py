from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import (
    UPS,
    AccessPoint,
    AccessPointLog,
    Camera,
    CameraLog,
    Desktop,
    DesktopLog,
    Firewall,
    FirewallLog,
    Laptop,
    LaptopLog,
    NVR,
    NVRLog,
    Router,
    RouterLog,
    Screen,
    ScreenLog,
    Server,
    ServerLog,
    Switch,
    SwitchLog,
    Telephone,
    TelephoneLog,
    UPSLog,
    VirtualMachine,
    VirtualMachineLog,
    ZKDevice,
    ZKDeviceLog,
)


def _user(instance):
    return getattr(instance, "_changed_by", None)


@receiver(post_save, sender=Laptop)
def log_laptop_create(sender, instance, created, **kwargs):
    if not created:
        return
    LaptopLog.objects.create(
        laptop=instance,
        changed_by=_user(instance),
        old_status=None,
        new_status=instance.status,
        old_employee=None,
        new_employee=instance.employee,
        on_hand_date=instance.on_hand_date,
        return_date=instance.return_date,
        branch=instance.branch,
    )


@receiver(pre_save, sender=Laptop)
def log_laptop_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Laptop.objects.get(pk=instance.pk)
    except Laptop.DoesNotExist:
        return
    if (
        old.status != instance.status
        or old.employee_id != instance.employee_id
        or old.branch_id != instance.branch_id
        or old.on_hand_date != instance.on_hand_date
        or old.return_date != instance.return_date
    ):
        LaptopLog.objects.create(
            laptop=instance,
            changed_by=_user(instance),
            old_status=old.status,
            new_status=instance.status,
            old_employee=old.employee,
            new_employee=instance.employee,
            on_hand_date=instance.on_hand_date,
            return_date=instance.return_date,
            branch=instance.branch,
        )


@receiver(post_save, sender=Desktop)
def log_desktop_create(sender, instance, created, **kwargs):
    if not created:
        return
    DesktopLog.objects.create(
        desktop=instance,
        changed_by=_user(instance),
        old_status=None,
        new_status=instance.status,
        old_employee=None,
        new_employee=instance.employee,
        on_hand_date=instance.on_hand_date,
        return_date=instance.return_date,
        branch=instance.branch,
    )


@receiver(pre_save, sender=Desktop)
def log_desktop_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Desktop.objects.get(pk=instance.pk)
    except Desktop.DoesNotExist:
        return
    if (
        old.status != instance.status
        or old.employee_id != instance.employee_id
        or old.branch_id != instance.branch_id
        or old.on_hand_date != instance.on_hand_date
        or old.return_date != instance.return_date
    ):
        DesktopLog.objects.create(
            desktop=instance,
            changed_by=_user(instance),
            old_status=old.status,
            new_status=instance.status,
            old_employee=old.employee,
            new_employee=instance.employee,
            on_hand_date=instance.on_hand_date,
            return_date=instance.return_date,
            branch=instance.branch,
        )


@receiver(post_save, sender=Screen)
def log_screen_create(sender, instance, created, **kwargs):
    if not created:
        return
    ScreenLog.objects.create(
        screen=instance,
        changed_by=_user(instance),
        old_status=None,
        new_status=instance.status,
        old_employee=None,
        new_employee=instance.employee,
        branch=instance.branch,
    )


@receiver(pre_save, sender=Screen)
def log_screen_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Screen.objects.get(pk=instance.pk)
    except Screen.DoesNotExist:
        return
    if (
        old.status != instance.status
        or old.employee_id != instance.employee_id
        or old.branch_id != instance.branch_id
    ):
        ScreenLog.objects.create(
            screen=instance,
            changed_by=_user(instance),
            old_status=old.status,
            new_status=instance.status,
            old_employee=old.employee,
            new_employee=instance.employee,
            branch=instance.branch,
        )


@receiver(post_save, sender=Telephone)
def log_telephone_create(sender, instance, created, **kwargs):
    if not created:
        return
    TelephoneLog.objects.create(
        telephone=instance,
        changed_by=_user(instance),
        old_status=None,
        new_status=instance.status,
        old_employee=None,
        new_employee=instance.employee,
        branch=instance.branch,
    )


@receiver(pre_save, sender=Telephone)
def log_telephone_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Telephone.objects.get(pk=instance.pk)
    except Telephone.DoesNotExist:
        return
    if (
        old.status != instance.status
        or old.employee_id != instance.employee_id
        or old.branch_id != instance.branch_id
    ):
        TelephoneLog.objects.create(
            telephone=instance,
            changed_by=_user(instance),
            old_status=old.status,
            new_status=instance.status,
            old_employee=old.employee,
            new_employee=instance.employee,
            branch=instance.branch,
        )


def _log_infra_create(log_model, fk_name, instance):
    log_model.objects.create(
        **{
            fk_name: instance,
            "changed_by": _user(instance),
            "old_status": None,
            "new_status": instance.status,
            "old_location": None,
            "new_location": instance.location or "",
            "old_branch": None,
            "new_branch": instance.branch,
            "comment": getattr(instance, "comment", None),
        }
    )


def _log_infra_update(model, log_model, fk_name, instance):
    if not instance.pk:
        return
    try:
        old = model.objects.get(pk=instance.pk)
    except model.DoesNotExist:
        return
    if (
        old.status != instance.status
        or old.location != instance.location
        or old.branch_id != instance.branch_id
    ):
        log_model.objects.create(
            **{
                fk_name: instance,
                "changed_by": _user(instance),
                "old_status": old.status,
                "new_status": instance.status,
                "old_location": old.location,
                "new_location": instance.location or "",
                "old_branch": old.branch,
                "new_branch": instance.branch,
                "comment": getattr(instance, "comment", None),
            }
        )


@receiver(post_save, sender=Camera)
def log_camera_create(sender, instance, created, **kwargs):
    if created:
        _log_infra_create(CameraLog, "camera", instance)


@receiver(pre_save, sender=Camera)
def log_camera_update(sender, instance, **kwargs):
    _log_infra_update(Camera, CameraLog, "camera", instance)


@receiver(post_save, sender=NVR)
def log_nvr_create(sender, instance, created, **kwargs):
    if created:
        _log_infra_create(NVRLog, "nvr", instance)


@receiver(pre_save, sender=NVR)
def log_nvr_update(sender, instance, **kwargs):
    _log_infra_update(NVR, NVRLog, "nvr", instance)


@receiver(post_save, sender=Firewall)
def log_firewall_create(sender, instance, created, **kwargs):
    if created:
        _log_infra_create(FirewallLog, "firewall", instance)


@receiver(pre_save, sender=Firewall)
def log_firewall_update(sender, instance, **kwargs):
    _log_infra_update(Firewall, FirewallLog, "firewall", instance)


@receiver(post_save, sender=Switch)
def log_switch_create(sender, instance, created, **kwargs):
    if created:
        _log_infra_create(SwitchLog, "switch", instance)


@receiver(pre_save, sender=Switch)
def log_switch_update(sender, instance, **kwargs):
    _log_infra_update(Switch, SwitchLog, "switch", instance)


@receiver(post_save, sender=AccessPoint)
def log_ap_create(sender, instance, created, **kwargs):
    if created:
        _log_infra_create(AccessPointLog, "access_point", instance)


@receiver(pre_save, sender=AccessPoint)
def log_ap_update(sender, instance, **kwargs):
    _log_infra_update(AccessPoint, AccessPointLog, "access_point", instance)


@receiver(post_save, sender=Router)
def log_router_create(sender, instance, created, **kwargs):
    if created:
        _log_infra_create(RouterLog, "router", instance)


@receiver(pre_save, sender=Router)
def log_router_update(sender, instance, **kwargs):
    _log_infra_update(Router, RouterLog, "router", instance)


@receiver(post_save, sender=ZKDevice)
def log_zk_create(sender, instance, created, **kwargs):
    if created:
        _log_infra_create(ZKDeviceLog, "device", instance)


@receiver(pre_save, sender=ZKDevice)
def log_zk_update(sender, instance, **kwargs):
    _log_infra_update(ZKDevice, ZKDeviceLog, "device", instance)


@receiver(post_save, sender=UPS)
def log_ups_create(sender, instance, created, **kwargs):
    if not created:
        return
    UPSLog.objects.create(
        ups=instance,
        changed_by=_user(instance),
        old_status=None,
        new_status=instance.status,
        old_location=None,
        new_location=instance.location or "",
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
    )


@receiver(pre_save, sender=UPS)
def log_ups_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = UPS.objects.get(pk=instance.pk)
    except UPS.DoesNotExist:
        return
    changed = (
        old.status != instance.status
        or old.location != instance.location
        or old.branch_id != instance.branch_id
        or old.voltage != instance.voltage
        or old.power_source != instance.power_source
        or old.last_maintenance_date != instance.last_maintenance_date
        or old.next_maintenance_date != instance.next_maintenance_date
    )
    if changed:
        UPSLog.objects.create(
            ups=instance,
            changed_by=_user(instance),
            old_status=old.status,
            new_status=instance.status,
            old_location=old.location,
            new_location=instance.location or "",
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
        )


@receiver(pre_save, sender=Server)
def log_server_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Server.objects.get(pk=instance.pk)
    except Server.DoesNotExist:
        return
    if (
        old.ip_address != instance.ip_address
        or old.cpu_cores != instance.cpu_cores
        or old.ram_gb != instance.ram_gb
        or old.storage_gb != instance.storage_gb
        or old.status != instance.status
        or old.location != instance.location
        or old.branch_id != instance.branch_id
    ):
        ServerLog.objects.create(
            server=instance,
            changed_by=_user(instance),
            old_status=old.status,
            new_status=instance.status,
            old_location=old.location,
            new_location=instance.location,
            old_branch=old.branch,
            new_branch=instance.branch,
            old_ip_address=old.ip_address,
            new_ip_address=instance.ip_address,
            old_cpu=old.cpu_cores,
            new_cpu=instance.cpu_cores,
            old_ram=old.ram_gb,
            new_ram=instance.ram_gb,
            old_storage=old.storage_gb,
            new_storage=instance.storage_gb,
        )


@receiver(pre_save, sender=VirtualMachine)
def log_vm_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = VirtualMachine.objects.get(pk=instance.pk)
    except VirtualMachine.DoesNotExist:
        return

    # Remember the previous host so its capacity can be released after the move.
    instance._previous_server_id = old.server_id

    changes = []
    if old.status != instance.status:
        changes.append(f"status {old.status}->{instance.status}")
    if (old.vcpu, old.vram_gb, old.storage_gb) != (
        instance.vcpu,
        instance.vram_gb,
        instance.storage_gb,
    ):
        changes.append(
            f"CPU {old.vcpu}->{instance.vcpu}, "
            f"RAM {old.vram_gb}->{instance.vram_gb}, "
            f"Storage {old.storage_gb}->{instance.storage_gb}"
        )
    if old.server_id != instance.server_id:
        changes.append(f"moved to server #{instance.server_id}")

    if changes:
        VirtualMachineLog.objects.create(
            vm=instance,
            old_status=old.status,
            new_status=instance.status,
            changed_by=_user(instance),
            comment="; ".join(changes),
        )


@receiver(post_save, sender=VirtualMachine)
def sync_server_on_vm_save(sender, instance, created, **kwargs):
    instance.server.update_available_resources()

    previous_server_id = getattr(instance, "_previous_server_id", None)
    if previous_server_id and previous_server_id != instance.server_id:
        previous = Server.objects.filter(pk=previous_server_id).first()
        if previous:
            previous.update_available_resources()
    instance._previous_server_id = None

    if created:
        VirtualMachineLog.objects.create(
            vm=instance,
            old_status=None,
            new_status=instance.status,
            changed_by=_user(instance),
            comment="VM created",
        )


@receiver(post_delete, sender=VirtualMachine)
def sync_server_on_vm_delete(sender, instance, **kwargs):
    server = Server.objects.filter(pk=instance.server_id).first()
    if server:
        server.update_available_resources()
