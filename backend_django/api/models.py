"""
Django models mirroring the original FastAPI Pydantic models.
Uses Django's ORM structure but data is stored in MongoDB.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid


class Enquiry(models.Model):
    """Enquiry model - mirrors EnquiryOut from FastAPI."""
    
    enquiry_no = models.IntegerField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    date_referred = models.DateField(null=True, blank=True)
    contact_person = models.CharField(max_length=200)
    company_name = models.CharField(max_length=300)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    requirement = models.CharField(max_length=100)
    premium_potential = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    tentative_brokerage_12pct = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    type_of_proposal = models.CharField(max_length=20, null=True, blank=True)
    expiry_date_existing_policy = models.DateField(null=True, blank=True)
    cre_rm_accountable = models.CharField(max_length=200)
    quote_planned_date = models.DateField(null=True, blank=True)
    quote_actual_date = models.DateField(null=True, blank=True)
    quote_submitted = models.CharField(max_length=3, default="No")
    closure_planned_date = models.DateField(null=True, blank=True)
    closure_actual_date = models.DateField(null=True, blank=True)
    business_closed = models.CharField(max_length=3, default="No")
    reason_not_closed = models.TextField(null=True, blank=True)
    fy = models.CharField(max_length=20, default="2025-26")
    branch = models.CharField(max_length=50, default="Ahmedabad")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "enquiries"
        ordering = ["enquiry_no"]
        indexes = [
            models.Index(fields=["cre_rm_accountable"]),
            models.Index(fields=["date_referred"]),
            models.Index(fields=["type_of_proposal"]),
            models.Index(fields=["business_closed"]),
            models.Index(fields=["fy", "branch"]),
        ]

    def __str__(self):
        return f"Enquiry #{self.enquiry_no} - {self.company_name}"

    def save(self, *args, **kwargs):
        if self.premium_potential:
            self.tentative_brokerage_12pct = round(float(self.premium_potential) * 0.12, 2)
        else:
            self.tentative_brokerage_12pct = 0
        super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    """Custom user manager for MongoDB-stored users."""

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    """Custom user model for authentication."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, default="viewer")  # admin or viewer
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username


class RefreshToken(models.Model):
    """Store refresh tokens for JWT authentication."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="refresh_tokens")
    token = models.CharField(max_length=500, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "refresh_tokens"

    def __str__(self):
        return f"Token for {self.user.username}"


class LoginAttempt(models.Model):
    """Track failed login attempts for rate limiting."""
    
    username = models.CharField(max_length=150)
    attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    last_attempt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "login_attempts"

    def __str__(self):
        return f"{self.username} - {self.attempts} attempts"