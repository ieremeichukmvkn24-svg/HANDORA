from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Address

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    
    # Додаємо наші кастомні поля у форму редагування користувача
    fieldsets = UserAdmin.fieldsets + (
        (_('Додаткова інформація'), {'fields': ('role', 'phone_number', 'avatar')}),
    )
    # Додаємо наші кастомні поля у форму створення користувача
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Додаткова інформація'), {'fields': ('email', 'role', 'phone_number')}),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'is_default')
    list_filter = ('is_default', 'city')
    search_fields = ('user__email', 'city', 'street')