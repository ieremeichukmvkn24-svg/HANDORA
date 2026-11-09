from django.shortcuts import render
from django.views.generic import DetailView
from django.core.paginator import Paginator
from .models import Product, Category

def product_list(request):
    # 1. Дістаємо всі категорії, щоб твій <aside> міг їх показати
    categories = Category.objects.all()
    
    # 2. Дістаємо всі активні товари
    products = Product.objects.filter(is_active=True)
    
    # 3. Фільтруємо товари, якщо натиснули на категорію (через ?category=slug)
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
        
    # 4. Пагінація
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/product_list.html', {
        'categories': categories,
        'products': page_obj.object_list,
        'page_obj': page_obj,
    })

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'