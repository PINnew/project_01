from django.urls import path
from .views import register, UserLoginView, LoginView, catalog, add_to_cart, cart, remove_from_cart, update_cart
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', catalog, name='home'),
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('catalog/', catalog, name='catalog'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),  # Страница корзины
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart/', update_cart, name='update_cart'),
]
