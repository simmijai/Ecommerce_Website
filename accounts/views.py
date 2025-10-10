from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views import View
from .forms import UserRegisterForm, UserLoginForm

class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home:home')
        return render(request, 'accounts/register.html', {'form': form})

class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home:home')
        return render(request, 'accounts/login.html', {'form': form})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:home')
