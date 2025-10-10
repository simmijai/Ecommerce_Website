from django.urls import path
from .views import CheckoutView, AddAddressView

app_name = 'orders'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-address/', AddAddressView.as_view(), name='add_address'),
]
