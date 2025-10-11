from django.shortcuts import render
from products.models import Category, Product

def home_view(request):
    # Get selected filters
    selected_category = request.GET.get('category')
    selected_subcategory = request.GET.get('subcategory')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    categories = Category.objects.filter(is_active=True)
    subcategories = Product.objects.none()  # Default empty

    products = Product.objects.filter(is_active=True)

    if selected_category:
        products = products.filter(subcategory__category_id=selected_category)
        subcategories = categories.get(id=selected_category).subcategories.all()

    if selected_subcategory:
        products = products.filter(subcategory_id=selected_subcategory)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        'categories': categories,
        'subcategories': subcategories,
        'products': products,
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'home/index.html', context)
