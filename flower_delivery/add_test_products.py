import os
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
django.setup()

from products.models import Product

# Словарь с тестовыми данными
test_products = [
    {"name": "Роза красная", "price": 100, "product_type": "rose", "color": "red", "image": "product_images/rose_r.jpg"},
    {"name": "Роза белая", "price": 100, "product_type": "rose", "color": "white", "image": "product_images/rose_white.jpg"},
    {"name": "Тюльпан жёлтый", "price": 80, "product_type": "tulip", "color": "yellow", "image": "product_images/tulip_yellow.jpg"},
    {"name": "Хризантема розовая", "price": 130, "product_type": "chrysanthemum", "color": "pink", "image": "product_images/chrysanthemum_pink.jpg"},
]

# Добавляем тестовые товары в базу данных
for product_data in test_products:
    product, created = Product.objects.get_or_create(
        name=product_data["name"],
        price=product_data["price"],
        product_type=product_data["product_type"],
        color=product_data["color"],
        image=product_data["image"],
    )
    if created:
        print(f'Товар "{product.name}" добавлен.')
    else:
        print(f'Товар "{product.name}" уже существует.')
