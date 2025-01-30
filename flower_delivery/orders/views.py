import asyncio
import logging
import threading
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync, sync_to_async
from django.shortcuts import render, redirect
from .models import Order
from products.models import Product
from bot.bot import send_order_notification


@login_required
def place_order_sync(request):
    """Синхронный метод для оформления заказа"""
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    if not products.exists():
        request.session['cart'] = []  # Очищаем корзину
        return redirect('cart')  # Перенаправляем обратно

    # Вычисляем итоговую сумму
    total_price = sum(product.price for product in products)

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

        # ✅ Отправляем уведомление в Telegram (асинхронно)
        asyncio.create_task(send_order_notification(order, total_price, products))

        # Перенаправляем на страницу успешного оформления заказа
        return redirect('order_success')

    return render(request, 'orders/place_order.html', {
        'products': products,
        'total_price': total_price,  # Передаём итоговую сумму в шаблон
    })


async def send_order_notification(order, total_price, products):
    # Асинхронная отправка уведомления в Telegram
    try:
        await some_async_telegram_api(order, total_price, products)
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке уведомления: {e}")


@sync_to_async
def some_async_telegram_api(order, total_price, products):
    # Синхронная реализация, если необходимо
    send_order_notification(order, total_price, products)


def order_success(request):
    """Страница успешного оформления заказа"""
    return render(request, 'orders/order_success.html')
