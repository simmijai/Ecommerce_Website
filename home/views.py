from django.shortcuts import render
from products.models import Category, Product

def home_view(request):
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    return render(request, 'home/index.html', {'categories': categories, 'products': products})
