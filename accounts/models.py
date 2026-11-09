from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Кастомна модель користувача для HANDORA.
    Замість username використовуємо email для авторизації.
    """
    class Role(models.TextChoices):
        BUYER = 'BUYER', _('Покупець')
        SELLER = 'SELLER', _('Продавець')
        ADMIN = 'ADMIN', _('Адміністратор')

    email = models.EmailField(_('Електронна пошта'), unique=True)
    phone_number = models.CharField(_('Номер телефону'), max_length=20, blank=True)
    role = models.CharField(
        _('Роль'), 
        max_length=10, 
        choices=Role.choices, 
        default=Role.BUYER
    )
    avatar = models.ImageField(_('Фото профілю'), upload_to='profiles/', blank=True, null=True)

    # Вказуємо, що логін відбувається через email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('Користувач')
        verbose_name_plural = _('Користувачі')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def is_seller(self):
        return self.role == self.Role.SELLER

    @property
    def is_buyer(self):
        return self.role == self.Role.BUYER

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(_('Місто'), max_length=100)
    street = models.CharField(_('Вулиця/Відділення'), max_length=255)
    is_default = models.BooleanField(_('За замовчуванням'), default=False)

    class Meta:
        verbose_name = _('Адреса')
        verbose_name_plural = _('Адреси')

    def __str__(self):
        return f"{self.city}, {self.street}"