"""API URL routing."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EnquiryViewSet, AnalyticsViewSet, LoginView,
    RefreshTokenView, LogoutView, UserViewSet,
)

router = DefaultRouter()
router.register(r"enquiries", EnquiryViewSet, basename="enquiry")
router.register(r"analytics", AnalyticsViewSet, basename="analytics")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/refresh", RefreshTokenView.as_view(), name="token_refresh"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("", include(router.urls)),
]