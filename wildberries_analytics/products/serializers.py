from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'sale_price', 'rating', 
            'reviews_count', 'discount', 'discount_amount',
            'query', 'brand', 'product_id', 'created_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_discount(self, obj):
        return obj.discount
    
    def get_discount_amount(self, obj):
        return obj.discount_amount