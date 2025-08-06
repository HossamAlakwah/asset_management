# admin.py
from django import forms
from django.apps import apps
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import (
    NVR,
    AccessPoint,
    Asset,
    Camera,
    Firewall,
    ReportableField,
    ReportableModel,
    Router,
    Screen,
    StorageDevice,
    Switch,
    Telephone,
)


class ReportableFieldAdminForm(forms.ModelForm):
    class Meta:
        model = ReportableField
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.model_id:
            reportable_model = self.instance.model
            try:
                app_label, model_name = reportable_model.model_path.split('.')
                model_class = apps.get_model(app_label, model_name)

                choices = []
                for field in model_class._meta.get_fields():
                    if not field.auto_created and hasattr(field, 'name'):
                        choices.append((field.name, field.verbose_name.title()))

                self.fields['field_name'] = forms.ChoiceField(
                    choices=choices,
                    initial=self.instance.field_name,
                    label='Field name',
                    help_text="Select a field from the model"
                )

            except Exception as e:
                raise ValidationError(f"Error loading model fields: {e}")




class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        exclude = ['created_by', 'created_at', 'updated_at','on_hand_date', 'return_date','branch','employee_name','status']
        widgets = {
            'warranty': forms.DateInput(attrs={'type': 'date'}),
        }
class StorageDeviceForm(forms.ModelForm):
    class Meta:
        model = StorageDevice
        exclude = ['asset']

StorageDeviceFormSet = inlineformset_factory(
    Asset, StorageDevice,
    form=StorageDeviceForm,
    extra=1,  
    min_num=1,
    validate_min=True,
)




class ScreenForm(forms.ModelForm):
    class Meta:
        model = Screen
        exclude = ['employee','created_by', 'created_at', 'updated_at', 'branch','status']
        widgets = {
            'warranty': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product'].required = True
        self.fields['serial'].required = True
        self.fields['brand'].required = True
'''
Telephone form
'''
class TelephoneForm(forms.ModelForm):
    class Meta:
        model = Telephone
        exclude = ['employee','created_by', 'created_at', 'updated_at', 'branch','status']
        widgets = {
            'warranty': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product'].required = True
        self.fields['serial'].required = True
        self.fields['brand'].required = True
        

'''

Cameras form

'''
class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        exclude = [
            'created_by', 'created_at', 'updated_at', 
            'branch', 'status', 'location'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }
    field_order = ['serial_number', 'model', 'power_source', 'ip_address', 'mac_address',  'purchase_date','comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].required = True
        self.fields['serial_number'].required = True
        self.fields['power_source'].required = True

class CameraEditForm(forms.ModelForm):
    class Meta:
        model = Camera
        exclude = ['created_by', 'created_at', 'updated_at']
    def __init__(self, *args, **kwargs):
        # Pop user from kwargs (make sure you pass it from the view)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Disable fields only for non-superadmins
        if not (user and hasattr(user, 'is_superadmin') and user.is_superadmin()):
            self.fields['serial_number'].disabled = True
            self.fields['purchase_date'].disabled = True
            self.fields['mac_address'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        print("Cleaned data:", cleaned_data)  # Add this

        status = cleaned_data.get('status')
        location = cleaned_data.get('location')
        print(status)
        if status == 'In Use' and not location:
            self.add_error('location', "Location is required when status is 'In Use'.")
        return cleaned_data
    
'''

NVR form

'''
class NVRForm(forms.ModelForm):
    class Meta:
        model = NVR
        exclude = [
            'created_by', 'created_at', 'updated_at', 
            'branch', 'status', 'location'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

    field_order = [
        'serial_number', 'model', 'hdd_capacity', 'number_of_ports',
        'ip_address', 'mac_address', 'purchase_date', 'comment'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].required = True
        self.fields['serial_number'].required = True
        self.fields['hdd_capacity'].required = True
        self.fields['number_of_ports'].required = True

class NVREditForm(forms.ModelForm):
    class Meta:
        model = NVR
        exclude = ['created_by', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['serial_number'].disabled = True
        self.fields['purchase_date'].disabled = True
        self.fields['mac_address'].disabled = True

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        location = cleaned_data.get('location')

        if status == 'In Use' and not location:
            self.add_error('location', "Location is required when status is 'In Use'.")

        return cleaned_data

''' Firewalls forms'''
class FirewallForm(forms.ModelForm):
    class Meta:
        model = Firewall
        exclude = [
            'created_by', 'created_at', 'updated_at',
            'branch', 'status', 'location'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

    field_order = [
        'serial_number', 'model', 'firmware_version', 'number_of_ports',
        'license_expiry', 'ip_address', 'mac_address', 'purchase_date', 'comment'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].required = True
        self.fields['serial_number'].required = True
        
class FirewallEditForm(forms.ModelForm):
    class Meta:
        model = Firewall
        exclude = ['created_by', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['serial_number'].disabled = True
        self.fields['purchase_date'].disabled = True
        # self.fields['mac_address'].disabled = True

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        location = cleaned_data.get('location')

        if status == 'In Use' and not location:
            self.add_error('location', "Location is required when status is 'In Use'.")

        return cleaned_data
    
'''
Switch Forms
'''


class SwitchForm(forms.ModelForm):
    class Meta:
        model = Switch
        exclude = [
            'created_by', 'created_at', 'updated_at',
            'branch', 'status', 'location'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

    field_order = [
        'serial_number', 'model', 'number_of_ports', 'number_of_poe_ports',
        'ip_address', 'mac_address', 'purchase_date', 'comment'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].required = True
        self.fields['serial_number'].required = True
        self.fields['number_of_ports'].required = True
        self.fields['number_of_poe_ports'].required = True

class SwitchEditForm(forms.ModelForm):
    ip_address = forms.GenericIPAddressField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. 192.168.0.1',
            'class': 'form-control',
        })
    )
    purchase_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        required=False,
        widget=forms.DateInput(
            attrs={'placeholder': 'DD-MM-YYYY', 'class': 'form-control'}
        )
    )
    class Meta:
        model = Switch
        exclude = ['created_by', 'created_at', 'updated_at']
        field_order = [
        'serial_number', 'model', 'number_of_ports', 'number_of_poe_ports',
        'ip_address', 'mac_address', 'purchase_date', 'comment'
    ]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Disable fields only for non-superadmins
        if not (user and hasattr(user, 'is_superadmin') and user.is_superadmin()):
            self.fields['serial_number'].disabled = True
            self.fields['purchase_date'].disabled = True
            self.fields['mac_address'].disabled = True

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        location = cleaned_data.get('location')

        if status == 'In Use' and not location:
            self.add_error('location', "Location is required when status is 'In Use'.")

        return cleaned_data

# Access Point creation form
class AccessPointForm(forms.ModelForm):
    class Meta:
        model = AccessPoint
        exclude = [
            'created_by', 'created_at', 'updated_at',
            'branch', 'status', 'location'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
    field_order = ['serial_number', 'model', 'ip_address', 'mac_address', 'purchase_date', 'expiry_date', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].required = True
        self.fields['serial_number'].required = True
        self.fields['expiry_date'].required = False  # optional, change if needed


# Access Point edit form
class AccessPointEditForm(forms.ModelForm):
    class Meta:
        model = AccessPoint
        exclude = ['created_by', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if not (user and hasattr(user, 'is_superadmin') and user.is_superadmin()):
            self.fields['serial_number'].disabled = True
            self.fields['purchase_date'].disabled = True
            self.fields['mac_address'].disabled = True
            self.fields['expiry_date'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        location = cleaned_data.get('location')

        if status == 'In Use' and not location:
            self.add_error('location', "Location is required when status is 'In Use'.")
        return cleaned_data

# Router creation form
class RouterForm(forms.ModelForm):
    class Meta:
        model = Router
        exclude = [
            'created_by', 'created_at', 'updated_at',
            'branch', 'status', 'location'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }
    field_order = ['serial_number', 'model', 'ip_address', 'mac_address', 'purchase_date', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].required = True
        self.fields['serial_number'].required = True


# Router edit form
class RouterEditForm(forms.ModelForm):
    class Meta:
        model = Router
        exclude = ['created_by', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if not (user and hasattr(user, 'is_superadmin') and user.is_superadmin()):
            self.fields['serial_number'].disabled = True
            self.fields['purchase_date'].disabled = True
            self.fields['mac_address'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        location = cleaned_data.get('location')

        if status == 'In Use' and not location:
            self.add_error('location', "Location is required when status is 'In Use'.")
        return cleaned_data
