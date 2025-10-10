from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Address
from .forms import AddressForm
from cart.models import Cart


# ✅ Checkout Page
class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()
        addresses = Address.objects.filter(user=user)
        context['cart'] = cart
        context['addresses'] = addresses
        context['cart_items'] = cart.items.all() if cart else []
        context['total_price'] = cart.total_price() if cart else 0
        return context


# ✅ Add New Address Form
class AddAddressView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'orders/add_address.html'
    success_url = reverse_lazy('orders:checkout')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
