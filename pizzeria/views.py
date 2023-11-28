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

#[{'pizza_id': 1, 'toppings': ['1']}, {'pizza_id': 1, 'toppings': ['2']}, {'pizza_id': 1, 'toppings': ['3']}, {'pizza_id': 1, 'toppings': []}, {'pizza_id': 2, 'toppings': ['2', '1', '3']}]
def get_cart(request):
    items_chosen = request.session.get('current_order', [])

    cart_list = []
    total_price = 0

    for element in items_chosen:
        pizza_choice = Pizza.objects.get(pk=element.get('pizza_id'))
        toppings_ids = element.get('toppings', [])

        if toppings_ids:
            toppings = Topping.objects.filter(pk__in=toppings_ids)
            toppings_list = [topping.name for topping in toppings]
            toppings_price_list = [topping.price for topping in toppings]
        else:
            toppings_list = []
            toppings_price_list = []
        json = {
            'pizza': pizza_choice.name,
            'toppings':toppings_list,
        }

        total_price += int(pizza_choice.price) + sum(toppings_price_list)
        cart_list.append(json)

    return render(request, template_name='pizzeria/cart.html', context={'cart_list': cart_list, 'price': total_price})

def delete_from_order(request, index):
    if 'current_order' in request.session:
        order = request.session['current_order']
        try:
            deleted_element = order.pop(index)
            request.session['current_order'] = order
            print(f"Deleted element at index {index} from the order: {deleted_element}")
        except IndexError:
            print(f"No element found at index {index} in the order.")

    return HttpResponseRedirect("/pizzeria/cart")

def get_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        customer_name = form.cleaned_data['name']
        if form.is_valid():
            return render(request, "pizzeria/thanks.html", {'name': customer_name})
