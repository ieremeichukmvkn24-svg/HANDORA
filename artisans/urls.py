from django.urls import path

app_name = 'artisans'

urlpatterns = [
    # Маршрути для майстрів додамо згодом
]

from django.urls import path
from . import views

app_name = 'artisans'

urlpatterns = [
    path('', views.artisan_list, name='artisan_list'),
    path('<slug:slug>/', views.artisan_detail, name='artisan_detail'),
]