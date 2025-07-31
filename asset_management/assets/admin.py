from django.contrib import admin

from assets.forms import CameraForm, NVRForm, ReportableFieldAdminForm

from .models import (
    NVR,
    Asset,
    AssetLog,
    Branch,
    Camera,
    CameraLog,
    Employee,
    Firewall,
    FirewallLog,
    NVRLog,
    Screen,
    ScreenLog,
)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
    list_display_links = ('id', 'name')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'title', 'email', 'creation_date', 'created_by')
    search_fields = ('name', 'email', 'department', 'title')
    ordering = ('-creation_date',)
    list_filter = ('department', 'title')
    list_display_links = ('id', 'name')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'serial', 'status', 'employee_name',
        'warranty', 'on_hand_date', 'return_date', 'branch',
        'type', 'created_at', 'updated_at'
    )
    search_fields = ('product', 'serial', 'employee_name__name')
    list_filter = ('status', 'type', 'branch', 'created_at')
    ordering = ('-created_at',)
    list_display_links = ('id', 'product', 'serial')
    list_select_related = ('employee_name', 'branch')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AssetLog)
class AssetLogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'asset', 'changed_by', 'old_status', 'new_status',
        'old_employee', 'new_employee', 'on_hand_date',
        'return_date', 'branch', 'change_time'
    )
    search_fields = (
        'asset__serial', 'changed_by__username',
        'old_employee__name', 'new_employee__name'
    )
    list_filter = ('new_status', 'branch', 'change_time')
    ordering = ('-change_time',)
    list_select_related = ('asset', 'changed_by', 'branch', 'old_employee', 'new_employee')
    readonly_fields = ('change_time',)

'''
Screens and pc-screens
'''


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ['product', 'serial', 'status', 'brand', 'employee', 'branch', 'created_at']
    list_filter = ['status', 'product', 'brand', 'branch']
    search_fields = ['serial', 'brand', 'employee__name']
    readonly_fields = ['created_at', 'updated_at', 'created_by']

@admin.register(ScreenLog)
class ScreenLogAdmin(admin.ModelAdmin):
    list_display = ['screen', 'new_status', 'old_employee', 'new_employee', 'branch', 'change_time']
    list_filter = ['new_status', 'branch']
    search_fields = ['screen__serial']
    
    
@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = (
        'model', 'serial_number', 'status',
        'location', 'ip_address', 'mac_address',
        'branch', 'purchase_date','branch'
    )
    list_filter = ('status', 'branch', 'power_source')
    search_fields = ('serial_number', 'model', 'ip_address', 'mac_address')
    readonly_fields = ('created_at', 'updated_at')




@admin.register(CameraLog)
class CameraLogAdmin(admin.ModelAdmin):
    list_display = (
        'camera', 'changed_by', 'change_time',
        'old_status', 'new_status',
        'old_location', 'new_location',
        'old_branch', 'new_branch'
    )
    list_filter = ('new_status', 'new_branch', 'change_time')
    search_fields = ('camera__serial_number', 'camera__model', 'changed_by__username')
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


@admin.register(NVR)
class NVRAdmin(admin.ModelAdmin):
    list_display = (
        'model', 'serial_number', 'status',
        'hdd_capacity', 'number_of_ports',
        'location', 'branch', 'purchase_date'
    )
    list_filter = ('status', 'branch')
    search_fields = ('serial_number', 'model')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(NVRLog)
class NVRLogAdmin(admin.ModelAdmin):
    list_display = (
        'nvr', 'changed_by', 'change_time',
        'old_status', 'new_status',
        'old_location', 'new_location',
        'old_branch', 'new_branch'
    )
    list_filter = ('new_status', 'new_branch', 'change_time')
    search_fields = ('nvr__serial_number', 'nvr__model', 'changed_by__username')
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
    
    
'''
Firewalls part
'''
@admin.register(Firewall)
class FirewallAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'firmware_version', 'number_of_ports', 'status', 'branch', 'created_by', 'created_at')
    search_fields = ('serial_number', 'model', 'ip_address', 'mac_address')
    list_filter = ('status', 'branch', 'created_by')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(FirewallLog)
class FirewallLogAdmin(admin.ModelAdmin):
    list_display = ('firewall', 'old_status', 'new_status', 'change_time', 'changed_by')
    search_fields = ('firewall__serial_number',)
    list_filter = ('new_status', 'changed_by', 'change_time')
    
'''
Dynamic Reports 
'''
# admin.py (continued)
from django.contrib import admin

from .models import ReportableField, ReportableModel


@admin.register(ReportableModel)
class ReportableModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_path']





from django import forms
from django.contrib import admin

from .models import ReportableField


class ReportableFieldAdminForm(forms.ModelForm):
    class Meta:
        model = ReportableField
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['field_name'] = forms.CharField(
            label='Field name',
            help_text="Will be populated automatically from model"
        )

    class Media:
        js = ('reportable_field_dynamic.js',)



@admin.register(ReportableField)
class ReportableFieldAdmin(admin.ModelAdmin):
    form = ReportableFieldAdminForm
