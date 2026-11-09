from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    
    # Цей рядок має бути ТУТ, у файлі, а не в терміналі:
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]

