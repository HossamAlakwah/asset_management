from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserChangeForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError

from .lockout import INVALID_LOGIN_MESSAGE, LOCKOUT_MESSAGE, is_locked, record_failure
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'first_name', 'last_name', 'phone')
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only super admin can create super admins or admins
        if user and not user.is_super_admin():
            self.fields['role'].choices = [('user', 'User')]

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'first_name', 'last_name', 'phone')

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )


class LockedAuthenticationForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": INVALID_LOGIN_MESSAGE,
        "locked": LOCKOUT_MESSAGE,
    }

    def clean(self):
        username = (self.data.get("username") or "").strip()
        if self.request and is_locked(self.request, username):
            raise ValidationError(
                self.error_messages["locked"],
                code="locked",
            )
        try:
            return super().clean()
        except ValidationError as exc:
            invalid = any(
                getattr(error, "code", None) == "invalid_login"
                for error in exc.error_list
            )
            if invalid and self.request:
                record_failure(self.request, username)
                if is_locked(self.request, username):
                    raise ValidationError(
                        self.error_messages["locked"],
                        code="locked",
                    ) from None
            raise