from django.db import models
from django.conf import settings
from mainapp.models import Product

# Create your models here.

class Order(models.Model):
    
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'
    
    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    created = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='дата обновления', auto_now=True)
    status = models.CharField(verbose_name='статус', max_length= 3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default= True)
    
    class Meta :
        ordering = ('-created',) # сортировка по умолчанию от более новых к старым заказам
        verbose_name = 'заказ' # имя класса в единственном числе
        verbose_name_plural = 'заказы' # имя класса во множественном числе
    
    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)
    
    def get_total_quantity (self):
        items = self.orderitems.select_related() # находим все элементы заказа
        return sum(list(map(lambda x: x.quantity, items)))
    
    def get_product_type_quantity (self):
        items = self.orderitems.select_related()
        return len(items)
    
    def get_total_cost (self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.product_cost, items)))
    
    # переопределяем метод, удаляющий объект
    def delete (self):
        for item in self.orderitems.select_related(): # находим все элементы заказа
            item.product.quantity += item.quantity # корректируем остатки продуктов на складе
            item.product.save()
        self.is_active = False
        self.save()
    
class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name= 'продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name= 'количество', default=0)
    
    @property
    def product_cost(self):
        return self.product.price * self.quantity