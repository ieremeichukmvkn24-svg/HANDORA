from decimal import Decimal

from django.conf import settings
from catalog.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(settings.CART_SESSION_ID, {})

    def add(self, product, quantity=1, override_quantity=False):
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError('Кількість товару має бути додатним цілим числом.')
        if not product.is_active or product.stock <= 0:
            raise ValueError('Товар недоступний.')

        product_id = str(product.pk)
        current = self.cart.get(product_id, {}).get('quantity', 0)
        new_quantity = quantity if override_quantity else current + quantity
        if new_quantity > product.stock:
            raise ValueError('Недостатньо товару на складі.')

        self.cart[product_id] = {
            'quantity': new_quantity,
            'price': str(product.price),
        }
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        key = str(product.pk)
        if key in self.cart:
            del self.cart[key]
            self.save()

    def __iter__(self):
        products = Product.objects.filter(pk__in=self.cart.keys())
        for product in products:
            item = self.cart[str(product.pk)]
            price = Decimal(item['price'])
            quantity = item['quantity']
            yield {
                'product': product,
                'quantity': quantity,
                'price': price,
                'total_price': price * quantity,
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            (Decimal(item['price']) * item['quantity'] for item in self.cart.values()),
            Decimal('0.00'),
        )

    def clear(self):
        self.session.pop(settings.CART_SESSION_ID, None)
        self.cart = {}
        self.save()
