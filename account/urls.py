# accounts/urls.py
from django.urls import path
from .views import SendOTPView, VerifyOTPView, ResendOTPView, UserAccountView, MyBusinessesView

urlpatterns = [
    path('login/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),

    path('account/', UserAccountView.as_view(), name='user_account'),
    path('account/my-businesses/', MyBusinessesView.as_view(), name='my_businesses'),
]
