# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    """Обробник для додавання товару в кошик"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Отримуємо кількість з форми (за замовчуванням 1)
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(product=product, quantity=quantity)
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """Обробник для видалення товару з кошика"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """Відображення сторінки кошика"""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})