from django.shortcuts import render, get_object_or_404
from .models import Artisan

def artisan_list(request):
    category = request.GET.get('category')
    artisans = Artisan.objects.filter(is_active=True)
    
    # Витягуємо унікальні категорії майстрів для фільтра
    categories = Artisan.objects.filter(is_active=True).values_list('category', flat=True).distinct()
    
    if category:
        artisans = artisans.filter(category=category)
        
    return render(request, 'artisans/artisan_list.html', {
        'artisans': artisans,
        'categories': categories,
        'selected_category': category
    })

def artisan_detail(request, slug):
    artisan = get_object_or_404(Artisan, slug=slug, is_active=True)
    # Отримуємо всі активні товари цього майстра (якщо зв'язок налаштовано)
    products = artisan.products.all() if hasattr(artisan, 'products') else []
    
    return render(request, 'artisans/artisan_detail.html', {
        'artisan': artisan,
        'products': products
    })