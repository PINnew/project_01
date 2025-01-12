from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView
from .models import Product


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Сразу логиним пользователя после регистрации
            return redirect('catalog')  # Перенаправляем на каталог после регистрации
    else:
        form = RegistrationForm()
    return render(request, 'products/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'products/login.html'


def catalog(request):
    products = Product.objects.all()
    return render(request, 'products/catalog.html', {'products': products})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect('catalog')
