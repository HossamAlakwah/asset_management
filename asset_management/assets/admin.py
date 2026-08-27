from django.contrib import admin

from .models import (
    UPS,
    AccessPoint,
    AccessPointLog,
    Branch,
    Camera,
    CameraLog,
    ColocationVM,
    Desktop,
    DesktopLog,
    Employee,
    Firewall,
    FirewallLog,
    Laptop,
    LaptopLog,
    NotificationConfig,
    NotificationRecipient,
    NVR,
    NVRLog,
    Router,
    RouterLog,
    Screen,
    ScreenLog,
    SentNotification,
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


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "choosable", "created_at")
    search_fields = ("name", "slug")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "department", "title", "email", "branch")
    search_fields = ("name", "email", "department")
    list_filter = ("branch", "department")


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ("serial", "product", "status", "employee", "branch", "created_at")
    search_fields = ("serial", "product", "employee__name")
    list_filter = ("status", "branch")
    list_select_related = ("employee", "branch")


@admin.register(LaptopLog)
class LaptopLogAdmin(admin.ModelAdmin):
    list_display = ("laptop", "old_status", "new_status", "changed_by", "change_time")
    list_select_related = ("laptop", "changed_by")


@admin.register(Desktop)
class DesktopAdmin(admin.ModelAdmin):
    list_display = ("serial", "product", "status", "employee", "branch", "created_at")
    search_fields = ("serial", "product", "employee__name")
    list_filter = ("status", "branch")
    list_select_related = ("employee", "branch")


@admin.register(DesktopLog)
class DesktopLogAdmin(admin.ModelAdmin):
    list_display = ("desktop", "old_status", "new_status", "changed_by", "change_time")


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ("serial", "product", "status", "brand", "employee", "branch")
    search_fields = ("serial", "brand")
    list_filter = ("status", "branch")


@admin.register(ScreenLog)
class ScreenLogAdmin(admin.ModelAdmin):
    list_display = ("screen", "new_status", "changed_by", "change_time")


@admin.register(Telephone)
class TelephoneAdmin(admin.ModelAdmin):
    list_display = ("serial", "product", "status", "brand", "employee", "branch")
    search_fields = ("serial", "brand", "product")
    list_filter = ("status", "branch")


@admin.register(TelephoneLog)
class TelephoneLogAdmin(admin.ModelAdmin):
    list_display = ("telephone", "new_status", "changed_by", "change_time")


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "model", "status", "ip_address", "branch")
    search_fields = ("serial_number", "model", "ip_address")
    list_filter = ("status", "branch")


@admin.register(CameraLog)
class CameraLogAdmin(admin.ModelAdmin):
    list_display = ("camera", "new_status", "changed_by", "change_time")


@admin.register(NVR)
class NVRAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "model", "status", "branch")
    search_fields = ("serial_number", "model")
    list_filter = ("status", "branch")


@admin.register(NVRLog)
class NVRLogAdmin(admin.ModelAdmin):
    list_display = ("nvr", "new_status", "changed_by", "change_time")


@admin.register(Firewall)
class FirewallAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "model", "status", "license_expiry_date", "branch")
    search_fields = ("serial_number", "model")
    list_filter = ("status", "branch")


@admin.register(FirewallLog)
class FirewallLogAdmin(admin.ModelAdmin):
    list_display = ("firewall", "new_status", "changed_by", "change_time")


@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "model", "status", "branch")
    search_fields = ("serial_number", "model")
    list_filter = ("status", "branch")


@admin.register(SwitchLog)
class SwitchLogAdmin(admin.ModelAdmin):
    list_display = ("switch", "new_status", "changed_by", "change_time")


@admin.register(AccessPoint)
class AccessPointAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "model", "status", "expiry_date", "branch")
    search_fields = ("serial_number", "model")
    list_filter = ("status", "branch")


@admin.register(AccessPointLog)
class AccessPointLogAdmin(admin.ModelAdmin):
    list_display = ("access_point", "new_status", "changed_by", "change_time")


@admin.register(Router)
class RouterAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "model", "status", "branch")
    search_fields = ("serial_number", "model")
    list_filter = ("status", "branch")


@admin.register(RouterLog)
class RouterLogAdmin(admin.ModelAdmin):
    list_display = ("router", "new_status", "changed_by", "change_time")


@admin.register(UPS)
class UPSAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "model", "status", "voltage", "branch")
    search_fields = ("serial_number", "model")
    list_filter = ("status", "branch")


@admin.register(UPSLog)
class UPSLogAdmin(admin.ModelAdmin):
    list_display = ("ups", "new_status", "changed_by", "change_time")


@admin.register(ZKDevice)
class ZKDeviceAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "device_type", "status", "ip_address", "branch")
    search_fields = ("serial_number", "model", "ip_address")
    list_filter = ("status", "device_type", "branch")


@admin.register(ZKDeviceLog)
class ZKDeviceLogAdmin(admin.ModelAdmin):
    list_display = ("device", "new_status", "changed_by", "change_time")


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("hostname", "serial_number", "status", "hypervisor", "branch")
    search_fields = ("hostname", "serial_number")
    list_filter = ("status", "hypervisor", "branch")
    readonly_fields = ("available_cpu_cores", "available_ram_gb", "available_storage_gb")


@admin.register(ServerLog)
class ServerLogAdmin(admin.ModelAdmin):
    list_display = ("server", "changed_by", "change_time")


@admin.register(VirtualMachine)
class VirtualMachineAdmin(admin.ModelAdmin):
    list_display = ("name", "server", "status", "environment", "vcpu", "vram_gb")
    search_fields = ("name", "ip_address", "server__hostname")
    list_filter = ("status", "environment", "server")


@admin.register(VirtualMachineLog)
class VirtualMachineLogAdmin(admin.ModelAdmin):
    list_display = ("vm", "old_status", "new_status", "changed_by", "change_time")


@admin.register(ColocationVM)
class ColocationVMAdmin(admin.ModelAdmin):
    list_display = ("name", "environment", "ip_address", "contract_end", "renewal_date")
    search_fields = ("name", "ip_address")
    list_filter = ("environment",)


@admin.register(NotificationConfig)
class NotificationConfigAdmin(admin.ModelAdmin):
    list_display = ("model_name", "condition_type", "condition_value", "is_active")
    list_filter = ("model_name", "is_active")


@admin.register(NotificationRecipient)
class NotificationRecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active")
    filter_horizontal = ("models_to_notify",)


@admin.register(SentNotification)
class SentNotificationAdmin(admin.ModelAdmin):
    list_display = ("config", "recipient", "triggered_by", "sent_at")
    readonly_fields = ("config", "recipient", "triggered_by", "message", "sent_at")
