from django.contrib import admin
from products.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'sale_price', 'rating', 'reviews_count', 'query')
    list_filter = ('query', 'brand', 'rating')
    search_fields = ('name', 'brand', 'query')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50