from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

from django.contrib.admin.sites import AdminSite


AdminSite.site_title = "Alireza"

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)
