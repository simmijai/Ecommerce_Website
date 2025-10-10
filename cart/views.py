# from django.shortcuts import get_object_or_404, redirect
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import ListView, DetailView, View, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from django.contrib import messages

# from .models import Cart, CartItem
# from products.models import Product
# from .forms import CartItemForm


# class CartListView(LoginRequiredMixin, ListView):
#     model = CartItem
#     template_name = "cart/cart_list.html"
#     context_object_name = "cart_items"

#     def get_queryset(self):
#         cart, _ = Cart.objects.get_or_create(user=self.request.user)
#         return cart.items.select_related('product')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cart, _ = Cart.objects.get_or_create(user=self.request.user)
#         context['total_price'] = cart.total_price()
#         return context


# class AddToCartView(LoginRequiredMixin, View):
#      def post(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         cart, _ = Cart.objects.get_or_create(user=request.user)
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#         if not created:
#             cart_item.quantity += 1
#             cart_item.save()
#         messages.success(request, f"{product.name} added to your cart.")
#         return redirect('cart:cart_list')


# class UpdateCartItemView(LoginRequiredMixin, UpdateView):
#     model = CartItem
#     form_class = CartItemForm
#     template_name = 'cart/cart_detail.html'

#     def form_valid(self, form):
#         messages.success(self.request, "Cart updated successfully!")
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy('cart:cart_list')


# class RemoveCartItemView(LoginRequiredMixin, DeleteView):
#     model = CartItem
#     success_url = reverse_lazy('cart:cart_list')

#     def delete(self, request, *args, **kwargs):
#         messages.success(request, "Item removed from cart.")
#         return super().delete(request, *args, **kwargs)


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Cart, CartItem
from products.models import Product
from .forms import CartItemForm


class CartListView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "cart/cart_list.html"
    context_object_name = "cart_items"
    login_url = '/accounts/login/'  # redirect if not logged in

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.select_related('product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context['total_price'] = cart.total_price()
        return context


class AddToCartView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, f"{product.name} added to your cart.")

        # redirect back to previous page (or home if referer missing)
        next_url = request.META.get('HTTP_REFERER', reverse_lazy('home:home'))
        return redirect(next_url)


class UpdateCartItemView(LoginRequiredMixin, UpdateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'cart/cart_detail.html'
    login_url = '/accounts/login/'

    def form_valid(self, form):
        messages.success(self.request, "Cart updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cart:cart_list')


class RemoveCartItemView(LoginRequiredMixin, DeleteView):
    model = CartItem
    success_url = reverse_lazy('cart:cart_list')
    login_url = '/accounts/login/'

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Item removed from cart.")
        return super().delete(request, *args, **kwargs)
