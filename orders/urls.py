from django.urls import path
from .views import CheckoutView, AddAddressView, OrderReviewView, PlaceOrderView, OrderHistoryView,OrderConfirmationView
from .views import AddAddressView, EditAddressView, DeleteAddressView

app_name = 'orders'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-address/', AddAddressView.as_view(), name='add_address'),
    path('order-review/', OrderReviewView.as_view(), name='order_review'),
    path('place-order/', PlaceOrderView.as_view(), name='place_order'),
            path('history/', OrderHistoryView.as_view(), name='order_history'),  # ✅ new
                path('order-confirmation/<int:order_id>/', OrderConfirmationView.as_view(), name='order_confirmation'),

path('add/', AddAddressView.as_view(), name='add_address'),
    path('edit/<int:pk>/', EditAddressView.as_view(), name='edit_address'),
    path('delete/<int:pk>/', DeleteAddressView.as_view(), name='delete_address'),

]

