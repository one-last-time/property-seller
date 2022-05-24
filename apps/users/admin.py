from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display =['pkid', 'id', 'email', 'first_name', 'last_name', 'username', 'is_staff', 'is_active']
    list_display_links = ['pkid', 'email']
    list_filter = ['first_name', 'last_name', 'email', 'username', 'is_active', 'is_staff']
    fieldsets = (
            (
                _('Login Credentials'),
                {
                    "fields": ("email", "password")
                }
            ),
            (
                _('Personal Information'),
                {
                    "fields": ('username', 'first_name', 'last_name')
                }
            ),
            (
                _('Permission and Groups'),
                {
                    "fields": ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
                }
            ),
            (
                _('Important dates'),
                {
                    'fields': ('date_joined', 'last_login')
                }
            )

    )
    add_fieldsets = (
        (None, {
            'classes': 'wide',
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields= ['email', 'username', 'first_name', 'last_name']


admin.site.register(User, UserAdmin)
