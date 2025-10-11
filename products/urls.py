from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView,
    CategoryUpdateView, CategoryDeleteView,
    SubCategoryListView, SubCategoryCreateView,
    SubCategoryUpdateView, SubCategoryDeleteView,
ProductListView, product_create_view, product_update_view, ProductDeleteView


)
from . import views
app_name = 'products'  # ✅ very important for namespacing


urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/add/", CategoryCreateView.as_view(), name="category-add"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category-edit"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category-delete"),
    
    path("subcategories/", SubCategoryListView.as_view(), name="subcategory-list"),
    path("subcategories/add/", SubCategoryCreateView.as_view(), name="subcategory-add"),
    path("subcategories/<int:pk>/edit/", SubCategoryUpdateView.as_view(), name="subcategory-edit"),
    path("subcategories/<int:pk>/delete/", SubCategoryDeleteView.as_view(), name="subcategory-delete"),
    
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/add/", product_create_view, name="product-add"),
    path("products/<int:pk>/edit/", product_update_view, name="product-edit"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),
    
    path('products/<slug:slug>/', views.product_detail_view, name='product-detail'),
        path('<slug:slug>/', views.product_detail_view, name='product_detail'),


]
