from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("orders/", views.get_pizza, name='orders'),
    path("orders/<int:pizza_id>/", views.get_topping, name='topping'),
    path("cart/", views.get_cart, name='cart'),
]