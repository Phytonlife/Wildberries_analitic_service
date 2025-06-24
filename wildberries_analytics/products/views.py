from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from products.models import Product
from products.serializers import ProductSerializer
from products.filters import ProductFilter
import numpy as np
from django.db.models import Count
import json

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = [
        'name', 'price', 'sale_price', 
        'rating', 'reviews_count', 'created_at'
    ]
    ordering = ['-created_at']

class PriceHistogramView(APIView):
    def get(self, request):
        filtered_queryset = ProductFilter(request.GET, queryset=Product.objects.all()).qs
        
        prices = [p.sale_price for p in filtered_queryset]
        if not prices:
            return Response({"bins": [], "counts": []})
        
        min_price, max_price = min(prices), max(prices)
        bin_size = max(1000, (max_price - min_price) / 10)
        
        bins = np.arange(min_price, max_price + bin_size, bin_size)
        counts, bins = np.histogram(prices, bins=bins)
        
        formatted_bins = [f"{int(bins[i])}-{int(bins[i+1])}" for i in range(len(bins)-1)]
        
        return Response({
            "bins": formatted_bins,
            "counts": counts.tolist(),
            "min_price": min_price,
            "max_price": max_price,
        })

class DiscountRatingView(APIView):
    def get(self, request):
        filtered_queryset = ProductFilter(request.GET, queryset=Product.objects.all()).qs
        
        data = [{
            "rating": p.rating,
            "discount": p.discount,
            "price": p.sale_price,
            "name": p.name,
            "id": p.id
        } for p in filtered_queryset]
        
        return Response(data)

class BrandsView(APIView):
    def get(self, request):
        brands = Product.objects.exclude(brand__isnull=True)\
                               .exclude(brand__exact='')\
                               .values('brand')\
                               .annotate(count=Count('brand'))\
                               .order_by('-count')
        return Response([b['brand'] for b in brands])