from django.db import models
from django.conf import settings

class Artisan(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='artisan_profile', 
        null=True, 
        blank=True
    )
    name = models.CharField(max_length=200, verbose_name="Ім'я / Назва майстерні")
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(
        max_length=100, 
        verbose_name="Категорія / Спеціалізація", 
        help_text="Наприклад: Кераміка, Шкіряні вироби, Деревообробка"
    )
    bio = models.TextField(verbose_name="Про майстра", blank=True)
    photo = models.ImageField(upload_to='artisans/', blank=True, null=True, verbose_name="Фото / Логотип")
    is_active = models.BooleanField(default=True, verbose_name="Показувати на сайті")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Майстер"
        verbose_name_plural = "Майстри"

    def __str__(self):
        return self.name

Shop = Artisan