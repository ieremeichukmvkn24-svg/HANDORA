from django.contrib import admin
from .models import Artisan

@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'category', 'bio']
    prepopulated_fields = {'slug': ('name',)}