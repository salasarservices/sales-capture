"""Django admin configuration for User model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, RefreshToken, LoginAttempt


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "role", "is_active", "is_staff", "created_at"]
    list_filter = ["role", "is_active", "is_staff"]
    search_fields = ["username"]
    ordering = ["-created_at"]
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("Dates", {"fields": ("created_at", "last_login")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password", "role"),
        }),
    )


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "expires_at", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__username"]
    ordering = ["-created_at"]


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ["username", "attempts", "locked_until", "last_attempt"]
    list_filter = ["attempts"]
    search_fields = ["username"]
    ordering = ["-last_attempt"]