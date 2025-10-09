# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("register/success/", views.register_success_view, name="register_success"),
    path("verify/<uidb64>/", views.verify_email_view, name="verify_email"),
    path('login/', views.login_view, name='login'),  # Make sure this exists

]
