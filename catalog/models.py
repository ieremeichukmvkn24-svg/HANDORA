from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from artisans.models import Shop

class Category(models.Model):
    """Модель категорії товарів"""
    name = models.CharField(_('Назва категорії'), max_length=100, unique=True)
    slug = models.SlugField(_('URL-посилання'), max_length=100, unique=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        blank=True, null=True, 
        related_name='subcategories',
        verbose_name=_('Батьківська категорія')
    )
    image = models.ImageField(_('Зображення категорії'), upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = _('Категорія')
        verbose_name_plural = _('Категорії')
        ordering = ['name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

class Product(models.Model):
    """Модель товару"""
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products', verbose_name=_('Магазин'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name=_('Категорія'))
    
    title = models.CharField(_('Назва виробу'), max_length=200)
    slug = models.SlugField(_('URL-посилання'), max_length=200, unique=True)
    description = models.TextField(_('Опис товару'))
    
    price = models.DecimalField(_('Ціна (₴)'), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_('Залишок на складі'), default=1)
    materials = models.CharField(_('Матеріали'), max_length=255, blank=True, help_text=_('Введіть через кому'))
    production_time = models.CharField(_('Час виготовлення'), max_length=100, blank=True, help_text=_('Наприклад: 3-5 днів'))
    
    is_active = models.BooleanField(_('Активний/Опублікований'), default=True)
    created_at = models.DateTimeField(_('Дата додавання'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата оновлення'), auto_now=True)

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товари')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_main_image(self):
        main_img = self.images.filter(is_main=True).first()
        if main_img:
            return main_img.image.url
        # Повертаємо перше ліпше фото, якщо головне не вказано
        first_img = self.images.first()
        return first_img.image.url if first_img else None


class ProductImage(models.Model):
    """Галерея зображень для товару"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('Товар'))
    image = models.ImageField(_('Зображення'), upload_to='products/%Y/%m/')
    is_main = models.BooleanField(_('Головне фото'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Фотографія товару')
        verbose_name_plural = _('Фотографії товарів')
        ordering = ['-is_main', '-created_at']

    def __str__(self):
        return f"Фото для {self.product.title}"