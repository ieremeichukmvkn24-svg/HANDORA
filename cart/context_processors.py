from .cart import Cart

def cart(request):
    """
    Додає об'єкт кошика в контекст усіх шаблонів.
    Тепер змінна {{ cart }} буде доступна скрізь.
    """
    return {'cart': Cart(request)}