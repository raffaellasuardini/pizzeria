from django.forms import ModelForm
from .models import OrderItem, Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address']


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['order']
