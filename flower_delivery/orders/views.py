from django.shortcuts import render, redirect
from .models import Order
from products.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def place_order(request):
    """Оформление заказа"""
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    if request.method == 'POST':
        # Получаем данные из формы
        delivery_address = request.POST['delivery_address']
        comment = request.POST.get('comment', '')

        # Создаём новый заказ
        order = Order.objects.create(
            user=request.user,
            delivery_address=delivery_address,
            comment=comment
        )
        order.products.set(products)
        order.save()

        # Очищаем корзину после оформления заказа
        request.session['cart'] = []

        # Перенаправляем на страницу успешного оформления заказа
        return redirect('order_success')

    return render(request, 'orders/place_order.html', {'products': products})


def order_success(request):
    """Страница успешного оформления заказа"""
    return render(request, 'orders/order_success.html')
