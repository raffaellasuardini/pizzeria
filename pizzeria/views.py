from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Pizza
from .forms import CustomerForm, OrderItemForm


def index(request):
    pizza_list = Pizza.objects.order_by('price')
    context = {"pizza_list": pizza_list}
    return render(request,'pizzeria/index.html', context)

def get_order(request):
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = OrderItemForm()
    return render(request,template_name='pizzeria/orders.html', context={"form": form})
def get_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        customer_name = form.cleaned_data['name']
        if form.is_valid():
            return render(request, "pizzeria/thanks.html", {'name': customer_name})