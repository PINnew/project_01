from django.shortcuts import render
from .models import Order
from products.models import Product


def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        products = Product.objects.filter(id__in=cart)
        order = Order.objects.create(
            user=request.user,
            delivery_address=request.POST['delivery_address'],
            comment=request.POST.get('comment', '')
        )
        order.products.set(products)
        order.save()
        request.session['cart'] = []  # Очищаем корзину после оформления заказа
        return redirect('order_success')
    else:
        return render(request, 'orders/place_order.html')
