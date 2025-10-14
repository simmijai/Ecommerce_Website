from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import User
from products.models import Product

def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, "You are not authorized as admin!")
        else:
            messages.error(request, "Invalid username or password!")
    return render(request, 'dashboard/login.html')

@login_required
def admin_logout_view(request):
    logout(request)
    return redirect('dashboard:admin-login')

@login_required
@user_passes_test(lambda u: u.is_staff)
def index(request):
    # ✅ Metrics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_products = Product.objects.count()

    # ✅ Low stock products (stock <= 5)
    low_stock_products = Product.objects.filter(stock__lte=5)

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'dashboard/index.html', context)


from products.models import Product
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_stock_view(request):
    products = Product.objects.all()

    if request.method == "POST":
        for product in products:
            new_stock = request.POST.get(f'stock_{product.id}')
            if new_stock is not None:
                product.stock = int(new_stock)
                product.save()
        return redirect('dashboard:edit-stock')

    context = {
        'products': products
    }
    return render(request, 'dashboard/edit_stock.html', context)


from accounts.models import User
from orders.models import Order  # assuming you have an Order model
from products.models import Product

@login_required
@user_passes_test(lambda u: u.is_staff)
def users_list_view(request):
    users = User.objects.all().order_by('-date_joined')  # latest users first

    context = {
        'users': users
    }
    return render(request, 'dashboard/users_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def user_detail_view(request, user_id):
    user = User.objects.get(id=user_id)
    # orders = user.order_set.all()  # all orders of this user
    orders = user.order_addresses.all()

    cart_items = user.cart_set.all() if hasattr(user, 'cart_set') else []

    context = {
        'user': user,
        'orders': orders,
        'cart_items': cart_items,
    }
    return render(request, 'dashboard/user_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def user_edit_view(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.is_active = bool(request.POST.get('is_active'))
        user.is_staff = bool(request.POST.get('is_staff'))
        user.save()
        return redirect('dashboard:users-list')

    context = {
        'user': user
    }
    return render(request, 'dashboard/user_edit.html', context)
