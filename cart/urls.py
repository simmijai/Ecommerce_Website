from django.urls import path
from .views import CartListView, AddToCartView, UpdateCartItemView, RemoveCartItemView

app_name = 'cart'

urlpatterns = [
    path('', CartListView.as_view(), name='cart_list'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('update/<int:pk>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('remove/<int:pk>/', RemoveCartItemView.as_view(), name='remove_cart_item'),
    
]
