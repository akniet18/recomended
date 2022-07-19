from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from users.models import User

class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_display = ('email', 'first_name', 'last_name',
                    'middle_name', 'birthday', 'country',
                    'region', 'city', 'is_staff', 'is_active',
                    'last_online', 'created_at')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {
            'fields': (
                'first_name', 'last_name', 'middle_name',
                'birthday', 'country', 'region', 'city',
                'gender'
                )
            }),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)