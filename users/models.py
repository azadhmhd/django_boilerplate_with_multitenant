import uuid

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.models import TenantModel


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    Provides methods for creating regular users and superusers.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model, extending Django's AbstractUser.
    """

    class AuthType(models.TextChoices):
        EMAIL = "EMAIL", "email"
        GOOGLE = "GOOGLE", "google"

    tenant_id = ''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    profile_pic = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    auth_type = models.CharField(max_length=255, blank=True, choices=AuthType.choices, default=AuthType.EMAIL)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def eligible_for_reset(self):
        """
        Check if the user is eligible for password reset.
        Returns True if the user is active and has a usable password,
        or if password usability check is disabled.
        """
        if not self.is_active:
            # if the user is active we don't bother checking
            return False

        if getattr(settings, 'DJANGO_REST_REQUIRE_USABLE_PASSWORD', True):
            # if we require a usable password then return the result of has_usable_password()
            return self.has_usable_password()
        else:
            # otherwise return True because we don't care about the result of has_usable_password()
            return True

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']


class Account(TenantModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    tenant_id = 'id'
    is_active = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    logo = models.CharField(max_length=255, null=True, blank=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TenantUser(TenantModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    tenant_id = 'account_id'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
