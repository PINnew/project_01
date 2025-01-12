from django.urls import path
from .views import register, UserLoginView, catalog, add_to_cart

urlpatterns = [
    path('', catalog, name='home'),  # Главная страница
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('catalog/', catalog, name='catalog'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
]
