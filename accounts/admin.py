from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Level


class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ('phone_number', 'user_address', 'level', 'profile_img'),}),
    )
    

admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Level)