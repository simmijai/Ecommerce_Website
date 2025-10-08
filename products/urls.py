from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView,
    CategoryUpdateView, CategoryDeleteView,
    SubCategoryListView, SubCategoryCreateView,
    SubCategoryUpdateView, SubCategoryDeleteView

)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/add/", CategoryCreateView.as_view(), name="category-add"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category-edit"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category-delete"),
    
    path("subcategories/", SubCategoryListView.as_view(), name="subcategory-list"),
    path("subcategories/add/", SubCategoryCreateView.as_view(), name="subcategory-add"),
    path("subcategories/<int:pk>/edit/", SubCategoryUpdateView.as_view(), name="subcategory-edit"),
    path("subcategories/<int:pk>/delete/", SubCategoryDeleteView.as_view(), name="subcategory-delete"),
]
