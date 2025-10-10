from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from cart.models import Cart, CartItem
from .models import Address, Order, OrderItem
from .forms import AddressForm

# -------------------------------
# 1️⃣ Checkout Page - Select Address
# -------------------------------
class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        addresses = user.addresses.all()  # get user addresses
        context['addresses'] = addresses
        return context

    def post(self, request, *args, **kwargs):
        selected_address_id = request.POST.get('selected_address')
        if not selected_address_id:
            messages.error(request, "Please select an address to continue.")
            return redirect('orders:checkout')

        request.session['selected_address'] = selected_address_id
        return redirect('orders:order_review')


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
# 3️⃣ Order Review Page
# -------------------------------
class OrderReviewView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()
        selected_address_id = self.request.session.get('selected_address')

        if not cart or not cart.items.exists():
            messages.error(self.request, "Your cart is empty.")
            return redirect('cart:cart_list')
        if not selected_address_id:
            messages.error(self.request, "No address selected.")
            return redirect('orders:checkout')

        shipping_address = Address.objects.get(id=selected_address_id)

        # prepare cart items with subtotal
        cart_items = []
        total_price = 0
        for item in cart.items.all():
            subtotal = item.product.price * item.quantity
            cart_items.append({
                'item': item,
                'subtotal': subtotal
            })
            total_price += subtotal

        context['cart_items'] = cart_items
        context['total_price'] = total_price
        context['shipping_address'] = shipping_address
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')
        if action and item_id:
            cart_item = CartItem.objects.filter(id=item_id, cart__user=request.user).first()
            if cart_item:
                if action == 'increase':
                    cart_item.quantity += 1
                    cart_item.save()
                elif action == 'decrease' and cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                elif action == 'remove':
                    cart_item.delete()
            return redirect('orders:order_review')

        # Proceed to place order
        return redirect('orders:place_order')


# -------------------------------
# 4️⃣ Place Order
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
        order_items = []
        for item in cart.items.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            order_items.append(order_item)

        # Clear Cart
        cart.items.all().delete()

        # Redirect to Order Confirmation page
        request.session['last_order_id'] = order.id
        return redirect('orders:order_confirmation')

class OrderConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('last_order_id')
        if not order_id:
            messages.error(self.request, "No order found.")
            return redirect('cart:cart_list')

        order = Order.objects.get(id=order_id)
        order_items = []

        for item in order.items.all():
            subtotal = item.price * item.quantity  # calculate subtotal in Python
            order_items.append({
                'product_name': item.product.name,
                'price': item.price,
                'quantity': item.quantity,
                'subtotal': subtotal
            })

        context['order'] = order
        context['order_items'] = order_items
        return context

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order

# -------------------------------
# 4️⃣ Order History
# -------------------------------
class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_history.html'
    context_object_name = 'orders'
    ordering = ['-created_at']  # show latest orders first

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
