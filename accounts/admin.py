from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {'fields': ('telefono',)}),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'telefono', 'is_staff')


admin.site.register(User, CustomUserAdmin)
