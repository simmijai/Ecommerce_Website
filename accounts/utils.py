# accounts/utils.py
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

# def send_verification_email(user):
#     token = str(random.randint(100000, 999999))
#     cache.set(f"verify_{user.email}", token, timeout=3600)  # 1 hour expiry

#     verification_link = f"http://localhost:8000/accounts/verify-email/?email={user.email}&token={token}"

#     subject = "Verify your email"
#     message = f"Hi {user.name},\nClick the link to verify your email:\n{verification_link}"
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def send_login_otp(user):
    otp = str(random.randint(100000, 999999))
    cache.set(f"login_{user.email}", otp, timeout=300)  # 5 mins expiry

    subject = "Your login OTP"
    message = f"Your login OTP is: {otp}. It expires in 5 minutes."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
    
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

def generate_verification_token(email):
    token = str(uuid.uuid4())
    cache.set(token, email, timeout=60*60)  # valid for 1 hour
    return token

def send_verification_email(name, email):
    token = generate_verification_token(email)
    verification_link = f"http://yourdomain.com/accounts/verify/{token}/"  # use your real domain
    subject = "Verify your email"
    message = f"Hi {name},\n\nClick the link below to verify your email:\n{verification_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

