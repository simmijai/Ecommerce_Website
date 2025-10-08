from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Category,SubCategory, Product, ProductImage, Variant
from .forms import CategoryForm,SubCategoryForm,ProductForm, ProductImageForm, VariantForm
from django.shortcuts import render,redirect



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
    
    

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm, ProductImageFormSet, VariantFormSet

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

def product_create_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)

            # ✅ Handle AnonymousUser
            if request.user.is_authenticated:
                product.created_by = request.user
            else:
                product.created_by = None

            product.save()

            image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
            if image_formset.is_valid():
                image_formset.save()

            variant_formset = VariantFormSet(request.POST, instance=product)
            if variant_formset.is_valid():
                variant_formset.save()

            return redirect('product-list')
    else:
        form = ProductForm()
        image_formset = ProductImageFormSet()
        variant_formset = VariantFormSet()

    return render(request, "products/product_form.html", {
        "form": form,
        "image_formset": image_formset,
        "variant_formset": variant_formset,
        "product": None
    })


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            if request.user.is_authenticated:
                product.created_by = request.user
            product.save()

            image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
            if image_formset.is_valid():
                image_formset.save()

            variant_formset = VariantFormSet(request.POST, instance=product)
            if variant_formset.is_valid():
                variant_formset.save()

            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
        image_formset = ProductImageFormSet(instance=product)
        variant_formset = VariantFormSet(instance=product)

    return render(request, "products/product_form.html", {
        "form": form,
        "image_formset": image_formset,
        "variant_formset": variant_formset,
        "product": product
    })


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("product-list")
