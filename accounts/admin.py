from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'unit', 'is_staff', 'is_active')
    list_filter = ('role', 'unit', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'unit')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'unit')}),
    )
