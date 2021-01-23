from django.conf.urls import include
from django.urls import path, re_path
import mainapp.views as mainapp
from django.views.decorators.cache import cache_page

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),
    re_path(r'^category/(?P<pk>\d+)/$', cache_page(3600)(mainapp.products), name='category'),
    # path('category/<int:pk>/', mainapp.products, name='category'),
    # path('category/<int:pk>/page/<int:page>/' , mainapp.products, name='page'),
    # path('product/<int:pk>/', mainapp.product, name='product'),
    path('product/<int:pk>/', mainapp.ProductDetailView.as_view(), name='product'),
    path('basket/', include('basketapp.urls', namespace='basket')),
]