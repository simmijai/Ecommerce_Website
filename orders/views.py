# orders/views.py
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from cart.models import Cart
from .models import Address, Order, OrderItem
from .forms import AddressForm


# -------------------------------
# 1️⃣ Checkout Page
# -------------------------------
class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()
        addresses = user.order_addresses.all()  # related_name in Address model
        context['cart'] = cart
        context['addresses'] = addresses
        context['cart_items'] = cart.items.all() if cart else []
        context['total_price'] = cart.total_price() if cart else 0
        return context

    def post(self, request, *args, **kwargs):
        """Handle selected address and redirect to place order"""
        selected_address_id = request.POST.get('selected_address')
        if not selected_address_id:
            messages.error(request, "Please select an address to continue.")
            return redirect('orders:checkout')
        
        request.session['selected_address'] = selected_address_id
        return redirect('orders:place_order')


# -------------------------------
# 2️⃣ Add New Address
# -------------------------------
class AddAddressView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'orders/add_address.html'
    success_url = reverse_lazy('orders:checkout')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Address added successfully!")
        return super().form_valid(form)


# -------------------------------
# 3️⃣ Place Order
# -------------------------------
class PlaceOrderView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        selected_address_id = request.session.get('selected_address')

        if not cart or not cart.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('cart:cart_list')

        if not selected_address_id:
            messages.error(request, "No address selected.")
            return redirect('orders:checkout')

        shipping_address = Address.objects.get(id=selected_address_id)

        # Create Order
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            total_price=cart.total_price()
        )

        # Create OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear Cart
        cart.items.all().delete()

        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('cart:cart_list')  # redirect back to cart or orders page
