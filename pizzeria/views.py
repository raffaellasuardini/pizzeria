from django.shortcuts import render
from .models import Pizza


def index(request):
    pizza_list = Pizza.objects.order_by('price')
    context = {"pizza_list": pizza_list}
    return render(request, 'pizzeria/index.html', context)
