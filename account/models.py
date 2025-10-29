from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number must be provided")
        extra_fields.setdefault("is_active", True)

        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # for OTP users
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Superuser must have a password")

        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = None  # remove default username field
    phone = models.CharField(max_length=15, unique=True)
    # name = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []  # no other required fields

    objects = CustomUserManager()

    def __str__(self):
        return self.phone
