from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Product


class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronica')

    def test_create_category(self):
        response = self.client.post('/api/categories/', {'name': 'Ropa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Ropa')

    def test_list_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Electronica')


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop 15 pulgadas, 16GB RAM',
            price=899.99,
        )

    def test_create_product(self):
        response = self.client.post('/api/products/', {
            'name': 'Mouse Gamer',
            'category': self.category.id,
            'description': 'Mouse RGB 6 botones',
            'price': 19.99,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data['category'], 'Electronica')

    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Laptop')

    def test_update_product(self):
        response = self.client.put(f'/api/products/{self.product.id}/', {
            'name': 'Laptop Pro',
            'category': self.category.id,
            'description': 'Laptop 15 pulgadas, 32GB RAM',
            'price': 1199.99,
        })
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Pro')
        self.assertEqual(str(self.product.price), '1199.99')

    def test_delete_product(self):
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    def test_filter_products_by_category(self):
        ropa = Category.objects.create(name='Ropa')
        Product.objects.create(name='Camisa', category=ropa, description='Camisa de algodon', price=25.50)
        response = self.client.get(f'/api/products/?category={ropa.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Camisa')

    def test_list_products_without_token(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 401)

    def test_precio_final_autenticado(self):
        response = self.client.get(f'/api/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 401)
