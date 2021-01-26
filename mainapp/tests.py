from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command

class TestMainappSmoke(TestCase):
   def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')        
        self.client = Client()

   def test_mainapp_urls(self):
       response = self.client.get('/')
       self.assertEqual(response.status_code, 200)

       response = self.client.get('/contact/')
       self.assertEqual(response.status_code, 200)

       response = self.client.get('/products/')
       self.assertEqual(response.status_code, 200)

       response = self.client.get('/products/category/0/')
       self.assertEqual(response.status_code, 200)

       for category in ProductCategory.objects.all():
           response = self.client.get(f'/products/category/{category.pk}/')
           self.assertEqual(response.status_code, 200)

       for product in Product.objects.all():
           response = self.client.get(f'/products/product/{product.pk}/')
           self.assertEqual(response.status_code, 200)

   def test_basket_login_redirect(self):
       # без логина должен переадресовать
       response = self.client.get('/basket/')
       self.assertEqual(response.url, '/auth/login/?next=/basket/')
       self.assertEqual(response.status_code, 302)

       # с логином все должно быть хорошо
       self.client.login(username='tarantino', password='geekbrains')

       response = self.client.get('/basket/')
       self.assertEqual(response.status_code, 200)
       self.assertEqual(list(response.context['basket']), [])
       self.assertEqual(response.request['PATH_INFO'], '/basket/')
       self.assertIn('Ваша корзина, Пользователь', response.content.decode())


   def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')