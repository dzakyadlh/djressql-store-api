from django.shortcuts import render
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.conf import settings

from .utils import response_formatter

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    cache_key = 'store:categories'

    def list(self, request, *args, **kwargs):
        data = cache.get(self.cache_key)

        if not data:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(self.cache_key, data)

        return response_formatter("Categories retrieved successfully", data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        cache.delete('store:categories')
        response = super().create(request, *args, **kwargs)
        return response_formatter("Category created successfully", response.data, status=response.status_code)

    def update(self, request, *args, **kwargs):
        cache.delete('store:categories')
        response = super().update(request, *args, **kwargs)
        return response_formatter("Category updated successfully", response.data, status=response.status_code)

    def destroy(self, request, *args, **kwargs):
        cache.delete('store:categories')
        response = super().destroy(request, *args, **kwargs)
        return response_formatter("Category deleted successfully", response.data, status=response.status_code)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    cache_key = 'store:products'

    def filter_products(self, queryset, category, price_min, price_max):
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        if price_min:
            try:
                price_min = float(price_min)
                queryset = queryset.filter(price__gte=price_min)
            except ValueError:
                pass

        if price_max:
            try:
                price_max = float(price_max)
                queryset = queryset.filter(price__lte=price_max)
            except ValueError:
                pass

        return queryset

    def list(self, request, *args, **kwargs):
        data = cache.get(self.cache_key)
        category = self.request.query_params.get('category')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')

        if not data or category or price_max or price_min:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(self.cache_key, data)
            serializer = self.get_serializer(self.filter_products(queryset, category, price_min, price_max), many=True)
            data = serializer.data

        return response_formatter("Products retrieved successfully", data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        cache.delete('store:products')
        response = super().create(request, *args, **kwargs)
        return response_formatter("Product created successfully", response.data, status=response.status_code)

    def update(self, request, *args, **kwargs):
        cache.delete('store:products')
        response = super().update(request, *args, **kwargs)
        return response_formatter("Product updated successfully", response.data, status=response.status_code)

    def destroy(self, request, *args, **kwargs):
        cache.delete('store:products')
        response = super().destroy(request, *args, **kwargs)
        return response_formatter("Product deleted successfully", response.data, status=response.status_code)
