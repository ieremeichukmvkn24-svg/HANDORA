from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    try:
        quantity = int(request.POST.get('quantity', '1'))
        Cart(request).add(product, quantity=quantity, override_quantity=request.POST.get("override") == "1")
    except (ValueError, TypeError) as exc:
        return HttpResponseBadRequest(str(exc))
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Cart(request).remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    return render(request, 'cart/cart_detail.html', {'cart': Cart(request)})
