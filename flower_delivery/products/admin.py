from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'color', 'price')  # Поля для отображения в списке
    list_filter = ('product_type', 'color')  # Фильтры для панели
    search_fields = ('name',)  # Поиск по названию
    ordering = ('product_type', 'color')  # Сортировка
    list_editable = ('price',)  # Возможность редактировать цену прямо из списка
    fields = ('name', 'product_type', 'color', 'price', 'image')  # Поля в форме редактирования
    readonly_fields = ()  # Поля, доступные только для чтения
