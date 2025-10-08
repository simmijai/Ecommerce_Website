from django import forms
from .models import Category, SubCategory, Product, ProductImage, Variant

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image']
        
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'slug', 'description', 'image']

from django.forms import inlineformset_factory
from .models import Product, ProductImage, Variant

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'subcategory', 'name', 'slug', 'sku', 'description',
            'price', 'discount_price', 'stock', 'quantity', 'brand', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_main']

class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['name', 'value', 'price', 'stock']

# Inline formsets for dynamic addition
ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm,
    extra=1, can_delete=True
)

VariantFormSet = inlineformset_factory(
    Product, Variant, form=VariantForm,
    extra=1, can_delete=True
)
