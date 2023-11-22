from django import forms
from .models import Pizza

class Customer(forms.Form):
    customer_name = forms.CharField(label="Your name", required=True, max_length=100)
    address = forms.CharField(label="Your address", required=True,max_length=100)

class Pizza(forms.Form):
    name = forms.ModelChoiceField(queryset=Pizza.objects.all())