from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Очищаємо кошик після створення замовлення
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    
    # Якщо кошик порожній, не дозволяємо оформити замовлення
    if len(cart) == 0:
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Зберігаємо замовлення (Order)
            order = form.save()
            
            # Перебираємо всі товари в кошику і створюємо OrderItem для кожного
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Очищаємо кошик після успішного оформлення
            cart.clear()
            
            # Відображаємо сторінку успішного оформлення
            return render(request, 'orders/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
        
    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})