from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Product

class CategoryAPITestCase(APITestCase):

    def test_create_category(self):
        data = {'name': 'Furniture', 'description': 'All types of furniture'}
        response = self.client.post('/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_categories(self):
        Category.objects.create(name='Books', description='Various books')
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_update_category(self):
        category = Category.objects.create(name='Toys', description='Children toys')
        data = {'name': 'Updated Toys', 'description': 'Updated description'}
        response = self.client.put(f'/api/categories/{category.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        category = Category.objects.create(name='Clothes', description='Various clothes')
        response = self.client.delete(f'/api/categories/{category.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductAPITestCase(APITestCase):

    def setUp(self):
        self.category1 = Category.objects.create(name='Drinks', description='Various drinks')
        self.category2 = Category.objects.create(name='Foods', description='Various foods')

    def test_create_product(self):
        data = {
            'name': 'Miro',
            'description': 'Chocolate milk',
            'price': 7000,
            'category': self.category1.id
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_products(self):
        Product.objects.create(name='Pochips', description='Potato chips', price=11000, category=self.category2)
        Product.objects.create(name='Supermilk', description='Cow milk', price=5000, category=self.category1)
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_update_product(self):
        product = Product.objects.create(
            name='Copico', 
            description='Coffee candy', 
            price=18000, 
            category=self.category1
        )
        data = {
            'name': 'Copico Black', 
            'description': 'Black coffee candy', 
            'price': 18000,
            'category': self.category1.id
        }
        response = self.client.put(f'/api/products/{product.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        product = Product.objects.create(
            name='Nata de polo', 
            description='Coconut drink', 
            price=20000, 
            category=self.category1
        )
        response = self.client.delete(f'/api/products/{product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
