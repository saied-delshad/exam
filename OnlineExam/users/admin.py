from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

from django.contrib.admin.sites import AdminSite


AdminSite.site_title = "CAA.IRI"

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'cell_phone', 'email', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'cell_phone',
          'photo')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser','user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
