# admin.py
from django import forms
from django.apps import apps
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import Asset, ReportableField, ReportableModel, Screen, StorageDevice


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

from django import forms

from .models import Asset, Screen


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

        # Explicitly mark which fields are required or not (optional)
        self.fields['product'].required = True
        self.fields['serial'].required = True
        self.fields['brand'].required = True
