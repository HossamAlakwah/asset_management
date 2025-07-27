from django.contrib import admin

from assets.forms import ReportableFieldAdminForm

from .models import Asset, AssetLog, Branch, Employee


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
