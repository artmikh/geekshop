from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length= 50, verbose_name= 'название категории', unique=True)
    description = models.TextField(max_length= 300, verbose_name= 'описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name= 'название категории')
    name = models.CharField(max_length=100, verbose_name= 'имя продукта')
    description = models.TextField(verbose_name= 'описание', blank=True)
    short_desc = models.CharField(max_length=40, verbose_name= 'краское описание', blank=True)
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(verbose_name= 'количество', default= 0)
    image = models.ImageField(upload_to='products_images', blank= True, verbose_name='картинка')
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')