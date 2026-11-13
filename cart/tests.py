from decimal import Decimal
from types import SimpleNamespace

from django.test import RequestFactory, TestCase
from django.contrib.sessions.middleware import SessionMiddleware

from artisans.models import Artisan
from catalog.models import Category, Product
from .cart import Cart


class CartTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        shop = Artisan.objects.create(name='Майстерня', slug='test-shop', category='Кераміка')
        category = Category.objects.create(name='Кераміка', slug='ceramics')
        cls.product = Product.objects.create(
            shop=shop, category=category, title='Чашка', slug='cup',
            description='Керамічна чашка', price=Decimal('150.00'),
            stock=5, is_active=True,
        )

    def setUp(self):
        request = RequestFactory().get('/')
        SessionMiddleware(lambda r: None).process_request(request)
        request.session.save()
        self.cart = Cart(request)

    def test_total_and_quantity(self):
        self.cart.add(self.product, 2)
        self.assertEqual(len(self.cart), 2)
        self.assertEqual(self.cart.get_total_price(), Decimal('300.00'))
        self.assertEqual(next(iter(self.cart))['total_price'], Decimal('300.00'))

    def test_override_quantity(self):
        self.cart.add(self.product, 2)
        self.cart.add(self.product, 3, override_quantity=True)
        self.assertEqual(len(self.cart), 3)

    def test_rejects_zero_and_more_than_stock(self):
        with self.assertRaises(ValueError):
            self.cart.add(self.product, 0)
        with self.assertRaises(ValueError):
            self.cart.add(self.product, 6)
        self.assertEqual(len(self.cart), 0)

    def test_remove_and_clear(self):
        self.cart.add(self.product)
        self.cart.remove(self.product)
        self.assertEqual(len(self.cart), 0)
        self.cart.add(self.product)
        self.cart.clear()
        self.assertEqual(len(self.cart), 0)
