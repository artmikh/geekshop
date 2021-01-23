import json
import os
import random
import basketapp
from basketapp.models import Basket
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mainapp.models import Product, ProductCategory
from django.views.generic.detail import DetailView
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.http import JsonResponse

# Create your views here.

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)

def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)

def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True ).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True ).select_related('category')

def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)

def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True , category__is_active=True ).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True , category__is_active=True ).order_by('price')

def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True , category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

def main(request):
    products = get_products()[:3]
    
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
    products = get_products()
    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products

def products(request, pk=None):
    title = "продукты"
    links_menu = get_links_menu()

    if pk:
        if pk == '0':
            products = get_products_orederd_by_price()
            category = {'name': 'все'}
        else:
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)

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

def products_ajax(request, pk=None, page= 1):
    if request.is_ajax():
        links_menu = get_links_menu()
        
        if pk:
            if pk == '0':
                category = {
                'pk': 0,
                'name': 'все'
                }
                products = get_products_orederd_by_price()
            else:
                category = get_category(pk)
                products = get_products_in_category_orederd_by_price(pk)

            # paginator = Paginator(products, 2)
            # try:
            #     products_paginator = paginator.page(page)
            # except PageNotAnInteger:
            #     products_paginator = paginator.page(1)
            # except EmptyPage:
            #     products_paginator = paginator.page(paginator.num_pages)
            
            content = {
                'links_menu': links_menu,
                'category': category,
                'products': products,
            }
            
            result = render_to_string('mainapp/includes/inc_products_list_content.html', context=content, request=request)
            
            return JsonResponse({'result': result})

class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product.html'

def product(request, pk):
    title = 'продукты'

    content = {
        'title':title,
        'links_menu':get_links_menu(),
        'product':get_product(pk),
        # 'basket': get_basket(request.user),  
    }

    return render(request, 'mainapp/product.html', content)

def load_from_json(file_name):
    # json_path = os.path.join(settings.BASE_DIR, 'mainapp/json')
    with open(os.path.join(settings.JSON_PATH, file_name + '.json'), 'r' ,errors='ignore') as infile:
        return json.load(infile)

def contact(request):
    if settings.LOW_CACHE:
        key = f'locations'
        locations = cache.get(key)
        if locations is None:
            locations = load_from_json('contact__locations')
            cache.set(key, locations)
    else:
        locations = load_from_json('contact__locations')

    
    content = {
        'title':'контакты',
        'contacts':locations,
        # 'basket': basket,
    }
    return render(request, 'mainapp/contact.html', content)
