from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from django.views.decorators.csrf import csrf_exempt


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Сразу логиним пользователя после регистрации
            return redirect('catalog')  # Перенаправляем на каталог после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'products/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'products/login.html'


def catalog(request):
    products = Product.objects.all()
    return render(request, 'products/catalog.html', {'products': products})


def add_to_cart(request, product_id):
    """Добавление товара в корзину с увеличением количества"""
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1  # Увеличиваем количество товара
    else:
        cart[str(product_id)] = 1  # Добавляем товар с количеством 1
    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    """Отображение корзины"""
    cart = request.session.get('cart', {})

    # Проверка: если корзина — это список, преобразуем в словарь
    if isinstance(cart, list):
        new_cart = {}
        for product_id in cart:
            new_cart[str(product_id)] = 1  # Устанавливаем количество 1 для каждого товара
        cart = new_cart
        request.session['cart'] = cart  # Сохраняем исправленную корзину

    products = Product.objects.filter(id__in=cart.keys())

    # Формируем список товаров с количеством
    cart_items = []
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)]
        })

    return render(request, 'products/cart.html', {'cart_items': cart_items})


def remove_from_cart(request, product_id):
    """Удаление товара из корзины"""
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]  # Удаляем товар из корзины
    request.session['cart'] = cart
    return redirect('cart')


@csrf_exempt
def update_cart(request):
    """Обновление количества товаров в корзине"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity > 0:
                        cart[product_id] = quantity
                except ValueError:
                    continue
        request.session['cart'] = cart
    return redirect('cart')