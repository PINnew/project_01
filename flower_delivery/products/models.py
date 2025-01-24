from django.db import models

class Product(models.Model):
    TYPE_CHOICES = [
        ('rose', 'Розы'),
        ('tulip', 'Тюльпаны'),
        ('chrysanthemum', 'Хризантемы'),
    ]
    COLOR_CHOICES = [
        ('red', 'Красные'),
        ('pink', 'Розовые'),
        ('white', 'Белые'),
        ('yellow', 'Жёлтые'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.name} ({self.get_product_type_display()}, {self.get_color_display()})"
