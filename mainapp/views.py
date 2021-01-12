import json
import os
import random
import basketapp
from basketapp.models import Basket
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mainapp.models import Product, ProductCategory

from django.views.generic.detail import DetailView

# Create your views here.



def main(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    products = Product.objects.all() [:4]
    
    content = {
        'title':'Главная',
        'products':products,
        # 'basket': basket,
    }
    return render(request, 'mainapp/index.html', content)

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products

def products(request, pk=None):
    title = "продукты"
    links_menu = ProductCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    
    if pk:
        if pk == '0':
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
            # 'basket': basket,
            }
        
        return render(request, 'mainapp/products_list.html', content)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')
        
        content = {
        'title': title,
        'links_menu': links_menu,
        'category': category,
        'products': products,
        # 'basket': basket,
        }
        
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title':'Продукты',
        'links_menu':links_menu,
        # 'basket': basket,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    
    return render(request, 'mainapp/products.html', content)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product.html'

def product(request, pk):
    title = 'продукт'

    content = {
        'title':title,
        'links_menu':ProductCategory.objects.all(),
        'product':get_object_or_404(Product, pk=pk),
        # 'basket': get_basket(request.user),  
    }

    return render(request, 'mainapp/product.html', content)

def contact(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    json_path = os.path.join(settings.BASE_DIR, 'mainapp/json')
    with open(os.path.join(json_path, 'contact__locations.json'), encoding='UTF-8') as json_file:
        contacts = json.load(json_file)
    content = {
        'title':'контакты',
        'contacts':contacts,
        # 'basket': basket,
    }
    return render(request, 'mainapp/contact.html', content)

