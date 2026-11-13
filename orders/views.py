from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from cart.cart import Cart
from catalog.models import Product
from .forms import OrderCreateForm
from .models import OrderItem


def order_create(request):
    cart = Cart(request)
    if not len(cart):
        return redirect('catalog:product_list')

    form = OrderCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        items = list(cart)
        try:
            with transaction.atomic():
                products = {
                    product.pk: product
                    for product in Product.objects.select_for_update().filter(
                        pk__in=[item['product'].pk for item in items]
                    )
                }
                for item in items:
                    product = products.get(item['product'].pk)
                    if not product or not product.is_active or item['quantity'] > product.stock:
                        raise ValueError(_('Недостатньо товару для оформлення замовлення.'))
                    if item['quantity'] <= 0:
                        raise ValueError(_('Некоректна кількість товару.'))

                order = form.save()
                for item in items:
                    product = products[item['product'].pk]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=item['quantity'],
                    )
                    product.stock -= item['quantity']
                    product.save(update_fields=['stock'])
        except ValueError as exc:
            form.add_error(None, str(exc))
        else:
            cart.clear()
            return render(request, 'orders/order_created.html', {'order': order})

    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})
