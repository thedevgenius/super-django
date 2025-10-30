# accounts/urls.py
from django.urls import path
from .views import SendOTPView, VerifyOTPView, ResendOTPView

urlpatterns = [
    path('login/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
]
