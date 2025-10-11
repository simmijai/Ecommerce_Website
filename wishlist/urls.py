# wishlist/urls.py
from django.urls import path
from .views import AddToWishlistView, WishlistListView, RemoveFromWishlistView

app_name = 'wishlist'

urlpatterns = [
    path('', WishlistListView.as_view(), name='view_wishlist'),
    path('add/<int:product_id>/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('remove/<int:product_id>/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
]
