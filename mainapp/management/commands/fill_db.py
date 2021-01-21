from django.core.management import BaseCommand
import os
from django.conf import settings
import json
from mainapp.models import ProductCategory, Product
from django.contrib.auth.models import User
from authapp.models import ShopUser

json_path = os.path.join(settings.BASE_DIR, 'mainapp/json')

def load_json_data(filename):
    with open(os.path.join(json_path, filename + '.json'), encoding='UTF-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        ProductCategory.objects.all().delete()
        categories = load_json_data('categories')
        for category in categories:
            ProductCategory.objects.create(**category)

        Product.objects.all().delete()
        products = load_json_data('products')
        for product in products:
            category_name = product['category']
            category_idx = ProductCategory.objects.get(name=category_name)
            product['category'] = category_idx
            Product.objects.create(**product)

        ShopUser.objects.create_superuser('django', 'django@yandex.ru', 'geekbrains', age=33)