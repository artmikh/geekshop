from django import forms
from ordersapp.models import Order, OrderItem
from mainapp.models import Product

class OrderForm(forms.ModelForm):
    class Meta :
        model = Order
        exclude = ('user',)
    
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

class OrderItemForm(forms.ModelForm):
    class Meta :
        model = OrderItem
        exclude = ()
    
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.get_items()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
    
    price = forms.CharField(label='цена', required= False)