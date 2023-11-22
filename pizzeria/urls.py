from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("orders/", views.get_order)
]