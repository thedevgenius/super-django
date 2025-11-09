# accounts/views.py
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.views import View
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone

from .models import User as CustomUser
from .forms import PhoneForm, OTPForm
from business.models import Business


def generate_otp():
    return str(random.randint(100000, 999999))


class SendOTPView(View):
    template_name = 'accounts/send_otp.html'

    def get(self, request):
        form = PhoneForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']

            otp = generate_otp()
            cache.set(f"otp_{phone}", otp, timeout=300)  # 5 mins expiry
            cache.set(f"otp_time_{phone}", timezone.now().timestamp(), timeout=300)

            # In production, send via SMS API (Twilio, MSG91, etc.)
            print(f"OTP for {phone}: {otp}")  # For development

            request.session['phone'] = phone
            messages.success(request, "OTP sent successfully!")
            return redirect('verify-otp')
        return render(request, self.template_name, {'form': form})


class VerifyOTPView(View):
    template_name = 'accounts/verify_otp.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Prevents direct access to /verify-otp/ unless phone exists in session.
        Works for both GET and POST.
        """
        phone = request.session.get('phone')
        if not phone:
            messages.warning(request, "Please enter your phone number first.")
            return redirect('send-otp')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = OTPForm()
        phone = request.session.get('phone')
        return render(request, self.template_name, {'form': form, 'phone': phone})

    def post(self, request):
        form = OTPForm(request.POST)
        phone = request.session.get('phone')

        if not phone:
            messages.error(request, "Session expired. Try again.")
            return redirect('send-otp')

        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            otp_stored = cache.get(f"otp_{phone}")

            if otp_stored and otp_entered == otp_stored:
                user, created = CustomUser.objects.get_or_create(phone=phone)
                user.is_phone_verified = True
                user.save()

                login(request, user)
                cache.delete(f"otp_{phone}")
                cache.delete(f"otp_time_{phone}")

                # Optional cleanup — remove phone from session after login
                del request.session['phone']

                messages.success(request, "Logged in successfully!")
                return redirect('home')
            else:
                messages.error(request, "Invalid or expired OTP.")
        return render(request, self.template_name, {'form': form, 'phone': phone})


class ResendOTPView(View):
    """Handles AJAX requests to resend OTP after 60 seconds"""

    def post(self, request):
        phone = request.session.get('phone')
        if not phone:
            return JsonResponse({'error': 'Session expired'}, status=400)

        last_sent = cache.get(f"otp_time_{phone}")
        now = timezone.now().timestamp()

        # Allow resend only after 60 seconds
        if last_sent and now - last_sent < 60:
            remaining = int(60 - (now - last_sent))
            return JsonResponse({'error': f'Please wait {remaining}s before resending OTP'}, status=429)

        otp = generate_otp()
        cache.set(f"otp_{phone}", otp, timeout=300)
        cache.set(f"otp_time_{phone}", now, timeout=300)

        # Send via SMS API (placeholder)
        print(f"Resent OTP for {phone}: {otp}")
        return JsonResponse({'success': 'OTP resent successfully'})


class UserAccountView(View):
    template_name = 'accounts/user_account.html'

    def get(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access your account.")
            return redirect('home')

        return render(request, self.template_name, {'user': request.user})
    

class MyBusinessesView(View):
    template_name = 'accounts/my_business.html'

    def get(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access your business dashboard.")
            return redirect('home')
        
        businesses = Business.objects.filter(owner=request.user)
        context = {
            'businesses': businesses
        }
        print(context)

        return render(request, self.template_name, context)