from django.db import models
from django.conf import settings
from products.models import Product  # Assuming Product model is in store app

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        return sum(item.quantity * item.product.price for item in self.items.all())
    

    def __str__(self):
        return f"Cart ({self.user.email})"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def item_total(self):
        return self.product.price * self.quantity  # 💰 Total for that item

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
