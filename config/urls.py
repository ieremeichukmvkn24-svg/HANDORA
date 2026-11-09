from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Підключені додатки
    path('accounts/', include('accounts.urls', namespace='accounts')), 
    path('artisans/', include('artisans.urls')),  # Підключили майстрів
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    
    # Головна сторінка (catalog) МАЄ БУТИ В КІНЦІ
    path('', include('catalog.urls', namespace='catalog')),
]

# Налаштування для відображення картинок під час розробки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)