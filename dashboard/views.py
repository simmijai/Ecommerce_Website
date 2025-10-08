from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # ✅ Only admin/staff can login
                login(request, user)
                return redirect('dashboard:dashboard')  # Because of app_name='dashboard'
            else:
                messages.error(request, "You are not authorized as admin!")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'dashboard/login.html')

@login_required
def admin_logout_view(request):
    logout(request)
    return redirect('dashboard:admin-login')

# Dashboard view - only for logged in admins
@login_required
@user_passes_test(lambda u: u.is_staff)
def index(request):
    return render(request, 'dashboard/index.html')

