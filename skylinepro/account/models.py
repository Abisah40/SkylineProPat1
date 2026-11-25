from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,PermissionsMixin
from django.conf import settings
from django.core.validators import RegexValidator,validate_email
import random
from datetime import timedelta
from django.utils import timezone
# phone_regex = RegexValidator( f"^\d{10}", message="phone number must be 10 digit"
# )


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    staff_id = models.CharField(max_length=30, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    username = None  # Remove the username field

    phone_number = models.CharField(max_length=15, blank=True, null=True,unique=True)
    email = models.EmailField(unique=True,blank=True, null=True, validators=[validate_email])
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)

    def generate_otp(self):
        # to generate otp
        self.otp = str(random.randint(100000, 999999))
        self.otp_expires_at = timezone.now() + timedelta(minutes=5)
        self.otp_verified = False
        self.save()


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.phone_number}"
    # @property
    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}"
