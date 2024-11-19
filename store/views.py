from django.shortcuts import render
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', 5)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    cache_key = 'store:categories'

    def list(self, request, *args, **kwargs):
        data = cache.get(self.cache_key)
        print("Cache GET for"+self.cache_key)

        if not data:
            # Serialize the queryset to JSON before caching
            data = list(self.queryset);
            cache.set(self.cache_key, data, CACHE_TTL)
            print(f"Cache set for"+self.cache_key)

        print('Cache retrieved')
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        cache.delete('store:categories')
        print(f"Cache deleted for"+self.cache_key)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        cache.delete('store:categories')
        print(f"Cache deleted for"+self.cache_key)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        cache.delete('store:categories')
        print(f"Cache deleted for"+self.cache_key)
        return super().destroy(request, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'store:products'
        data = cache.get(cache_key)

        if not data:
            data = list(self.queryset)
            cache.set(cache_key, data, CACHE_TTL)

        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        cache.delete('store:products')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        cache.delete('store:products')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        cache.delete('store:products')
        return super().destroy(request, *args, **kwargs)
