from django.urls import path
from products.views import ProductListView, PriceHistogramView, DiscountRatingView, BrandsView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/histogram/', PriceHistogramView.as_view(), name='price-histogram'),
    path('products/discount-rating/', DiscountRatingView.as_view(), name='discount-rating'),
    path('products/brands/', BrandsView.as_view(), name='brands-list'),
]