from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    toppings = models.ManyToManyField(Topping, through='PizzaTopping', blank=True)

    def __str__(self):
        return self.name


class PizzaTopping(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.topping.name} on {self.pizza.name}"


class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        # Update the order total price when saving an order item
        self.item_price = self.pizza.price * self.quantity
        self.order.total_price += self.item_price
        self.order.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.pizza.name} in Order #{self.order.id}"
