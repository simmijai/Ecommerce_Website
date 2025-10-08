from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Category,SubCategory
from .forms import CategoryForm,SubCategoryForm

class CategoryListView(ListView):
    model = Category
    template_name = "products/category_list.html"
    context_object_name = "categories"

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("category-list")

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("category-list")

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "products/category_confirm_delete.html"
    success_url = reverse_lazy("category-list")

class SubCategoryListView(ListView):
    model = SubCategory
    template_name = "products/subcategory_list.html"
    context_object_name = "subcategories"

class SubCategoryCreateView(CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "products/subcategory_form.html"
    success_url = reverse_lazy("subcategory-list")

class SubCategoryUpdateView(UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "products/subcategory_form.html"
    success_url = reverse_lazy("subcategory-list")

class SubCategoryDeleteView(DeleteView):
    model = SubCategory
    template_name = "products/subcategory_confirm_delete.html"
    success_url = reverse_lazy("subcategory-list")
