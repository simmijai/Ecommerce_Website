from django.urls import path
from .views import CheckoutView, AddAddressView, PlaceOrderView

app_name = 'orders'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-address/', AddAddressView.as_view(), name='add_address'),
    path('place-order/', PlaceOrderView.as_view(), name='place_order'),
]
