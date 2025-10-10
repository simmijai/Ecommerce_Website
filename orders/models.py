# orders/models.py
from django.db import models
from django.conf import settings


from django.db import models
from accounts.models import User, Address
from products.models import Product, Variant


# -------------------------------
# 1️⃣ ORDER MODEL
# -------------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_addresses")
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def calculate_total(self):
        """Calculate and update total order price"""
        total = sum(item.total_price() for item in self.items.all())
        self.total_price = total
        self.save()
        return total


# -------------------------------
# 2️⃣ ORDER ITEM MODEL
# -------------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # locked price at purchase

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def total_price(self):
        return self.price * self.quantity
