# accounts/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.urls import reverse
from .forms import RegisterForm
from .models import User

# ----------------- Register -----------------
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False   # deactivate until verified
            user.save()

            # Generate verification link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = request.build_absolute_uri(
                reverse('accounts:verify_email', kwargs={'uidb64': uid})
            )

            # Send email
            send_mail(
                subject='Verify your email',
                message=f'Click this link to verify your account: {link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            messages.success(request, "Check your email to verify your account.")
            return redirect('accounts:register_success')
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

# ----------------- Email verification -----------------
def verify_email_view(request, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user.is_active = True
        user.is_verified = True
        user.save()
        messages.success(request, "Email verified! You can now login.")
        return redirect('accounts:login')
    except Exception:
        messages.error(request, "Verification link is invalid.")
        return redirect('accounts:register')

# ----------------- Register success page -----------------
def register_success_view(request):
    return render(request, "accounts/register_success.html")

from django.shortcuts import render

def login_view(request):
    return render(request, 'accounts/login.html')

from django.shortcuts import render
from django.core.cache import cache
from .models import User

def verify_email(request, token):
    email = cache.get(token)
    if email:
        try:
            user = User.objects.get(email=email)
            user.is_verified = True
            user.is_active = True
            user.save()
            cache.delete(token)
            return render(request, "accounts/verify_success.html")
        except User.DoesNotExist:
            pass
    return render(request, "accounts/verify_failed.html")
