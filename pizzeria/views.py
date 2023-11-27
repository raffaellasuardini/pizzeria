from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Pizza, Topping
from .forms import CustomerForm


def index(request):
    pizza_list = Pizza.objects.order_by('price')
    context = {"pizza_list": pizza_list}
    return render(request, 'pizzeria/index.html', context)


def get_pizza(request):
    pizza_list = Pizza.objects.order_by('price')
    return render(request, template_name='pizzeria/orders.html', context={"pizza_list": pizza_list})


def get_topping(request, pizza_id):
    topping_list = Topping.objects.order_by('price')
    current_pizza = get_object_or_404(Pizza, pk=pizza_id)

    if request.method == 'POST':
        selected_toppings_id = request.POST.getlist('topping')
        json = {'pizza_id': pizza_id, 'toppings': selected_toppings_id}
        if 'current_order' in request.session:
            order = request.session.get('current_order')
            order.append(json)
            print('ho aggiunto')
            request.session['current_order'] = order

        else:
            request.session['current_order'] = [json]

        print(request.session['current_order'])
        return HttpResponseRedirect("/pizzeria/orders")
    else:
        context = {'topping_list': topping_list, 'pizza': current_pizza}
    return render(request, template_name='pizzeria/topping.html', context=context)


def get_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        customer_name = form.cleaned_data['name']
        if form.is_valid():
            return render(request, "pizzeria/thanks.html", {'name': customer_name})
