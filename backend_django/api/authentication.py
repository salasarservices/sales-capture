"""
JWT Authentication for Django REST Framework.
Mirrors the FastAPI auth.py logic from the original codebase.
"""

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import authentication, exceptions
from .models import User, RefreshToken


class JWTAuthentication(authentication.BaseAuthentication):
    """Custom JWT authentication class."""

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                return None
        except ValueError:
            return None

        return self.authenticate_token(token)

    def authenticate_token(self, token: str):
        """Validate JWT token and return (user, token)."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            user_id = payload.get("user_id")
            if not user_id:
                raise exceptions.AuthenticationFailed("Invalid token")

            user = User.objects.filter(id=user_id).first()
            if not user or not user.is_active:
                raise exceptions.AuthenticationFailed("User not found or inactive")

            return (user, token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")


def generate_access_token(user: User) -> str:
    """Generate JWT access token."""
    expire = timezone.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": str(user.id),
        "username": user.username,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def generate_refresh_token(user: User) -> str:
    """Generate JWT refresh token and store in database."""
    expire = timezone.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    token = jwt.encode(
        {"user_id": str(user.id), "exp": expire, "type": "refresh"},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    RefreshToken.objects.create(user=user, token=token, expires_at=expire)
    return token


def verify_refresh_token(token: str) -> User:
    """Verify refresh token and return user."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload.get("type") != "refresh":
            raise exceptions.AuthenticationFailed("Invalid token type")

        refresh_token = RefreshToken.objects.filter(token=token).first()
        if not refresh_token or refresh_token.expires_at < timezone.now():
            raise exceptions.AuthenticationFailed("Token expired or invalid")

        return refresh_token.user
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed("Invalid token")


def revoke_refresh_token(token: str):
    """Revoke a refresh token."""
    RefreshToken.objects.filter(token=token).delete()