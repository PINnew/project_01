from django.shortcuts import render, redirect
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

    # Проверка: если корзина хранится как список, преобразуем её в словарь
    if isinstance(cart, list):
        new_cart = {}
        for id in cart:
            new_cart[str(id)] = 1  # Устанавливаем количество 1 для каждого товара
        cart = new_cart
        request.session['cart'] = cart  # Сохраняем преобразованную корзину

    # Добавляем товар или увеличиваем его количество
    if str(product_id) in cart:
        cart[str(product_id)] += 1  # Увеличиваем количество
    else:
        cart[str(product_id)] = 1  # Добавляем товар с количеством 1

    # Обновляем корзину в сессии
    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    """Отображение корзины"""
    cart = request.session.get('cart', {})

    # Проверка, если корзина вдруг сохранилась как список (устаревший формат)
    if isinstance(cart, list):
        new_cart = {}
        for product_id in cart:
            new_cart[str(product_id)] = 1  # Количество по умолчанию 1
        cart = new_cart
        request.session['cart'] = cart  # Обновляем в сессии

    products = Product.objects.filter(id__in=cart.keys())

    # Формируем список товаров с количеством
    cart_items = []
    total_price = 0  # Переменная для итоговой суммы
    for product in products:
        quantity = cart[str(product.id)]
        total_price += product.price * quantity  # Добавляем стоимость товара в итог
        cart_items.append({
            'product': product,
            'quantity': quantity,
        })

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,  # Передаём в шаблон
    })


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