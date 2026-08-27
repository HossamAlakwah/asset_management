from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, LoginLock, TwoFactorDevice


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(LoginLock)
class LoginLockAdmin(admin.ModelAdmin):
    list_display = ("kind", "value", "failures", "locked_until", "updated_at")
    list_filter = ("kind",)
    search_fields = ("value",)
    readonly_fields = ("kind", "value", "failures", "window_started", "updated_at")

    def has_add_permission(self, request):
        return False


@admin.register(TwoFactorDevice)
class TwoFactorDeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "confirmed", "confirmed_at")
    list_filter = ("confirmed",)
    search_fields = ("user__username",)
    readonly_fields = ("user", "confirmed", "confirmed_at")
    exclude = ("secret", "backup_hashes")

    def has_add_permission(self, request):
        return False


admin.site.register(CustomUser, CustomUserAdmin)
