# wishlist/views.py
from django.views import View
from django.views.generic import ListView
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product
from .models import Wishlist


class AddToWishlistView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        if created:
            messages.success(request, "Product added to your wishlist!")
        else:
            messages.info(request, "This product is already in your wishlist.")

        # ✅ FIX: use product slug for redirect (not product_id)
        return redirect('home:home')


class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'wishlist/wishlist.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Wishlist.objects.filter(user=request.user, product=product).delete()
        messages.success(request, "Product removed from wishlist.")
        return redirect('wishlist:view_wishlist')
