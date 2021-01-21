from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    # path('', basketapp.basket, name='view'),
    path('', basketapp.BasketListView.as_view(), name='view'),
    path('add/<int:pk>/', basketapp.add, name='add'),
    path('delete/<int:pk>/', basketapp.delete, name='delete'),
    path('edit/<int:pk>/<int:quantity>/', basketapp.edit, name='edit')
    
]

