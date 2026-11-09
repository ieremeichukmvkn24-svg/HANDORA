from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    """Дозволяє додавати фотографії прямо у картці товару в адмінці"""
    model = ProductImage
    extra = 1  # Кількість порожніх форм для нових фото

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'category', 'price', 'stock', 'is_active')
    list_filter = ('is_active', 'category', 'shop')
    search_fields = ('title', 'description', 'shop__name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]
    
    # Робимо поля shop та category зручнішими для вибору (якщо їх багато)
    autocomplete_fields = ['shop', 'category']