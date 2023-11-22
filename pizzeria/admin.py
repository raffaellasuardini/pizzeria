from django.contrib import admin
from .models import Topping, Pizza, PizzaTopping, Customer, Order, OrderItem

admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(PizzaTopping)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)