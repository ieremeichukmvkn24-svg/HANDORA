from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from artisans.models import Artisan
from catalog.models import Category, Product
from .models import Order, OrderItem


class CheckoutTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        shop = Artisan.objects.create(name='Майстерня', slug='order-shop', category='Декор')
        category = Category.objects.create(name='Декор', slug='decor')
        cls.product = Product.objects.create(
            shop=shop, category=category, title='Свічка', slug='candle',
            description='Авторська свічка', price=Decimal('100.00'), stock=3,
        )

    def form_data(self):
        return {
            'first_name': 'Олена', 'last_name': 'Петренко',
            'email': 'olena@example.com', 'phone': '+380501234567',
            'address': 'Відділення 1', 'city': 'Рівне',
        }

    def test_empty_cart_cannot_create_order(self):
        response = self.client.post(reverse('orders:order_create'), self.form_data())
        self.assertRedirects(response, reverse('catalog:product_list'))
        self.assertFalse(Order.objects.exists())

    def test_successful_checkout_creates_items_decrements_stock_and_clears_cart(self):
        self.client.post(reverse('cart:cart_add', args=[self.product.pk]), {'quantity': 2})
        response = self.client.post(reverse('orders:order_create'), self.form_data())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_created.html')
        order = Order.objects.get()
        item = OrderItem.objects.get(order=order)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, Decimal('100.00'))
        self.assertEqual(order.get_total_cost(), Decimal('200.00'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
        self.assertNotIn('cart', self.client.session)

    def test_stock_reduction_prevents_checkout(self):
        self.client.post(reverse('cart:cart_add', args=[self.product.pk]), {'quantity': 2})
        Product.objects.filter(pk=self.product.pk).update(stock=1)
        response = self.client.post(reverse('orders:order_create'), self.form_data())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Недостатньо товару')
        self.assertFalse(Order.objects.exists())
        self.assertEqual(self.client.session['cart'][str(self.product.pk)]['quantity'], 2)

    def test_invalid_form_does_not_create_order(self):
        self.client.post(reverse('cart:cart_add', args=[self.product.pk]), {'quantity': 1})
        data = self.form_data()
        data['email'] = 'bad-email'
        response = self.client.post(reverse('orders:order_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.exists())
