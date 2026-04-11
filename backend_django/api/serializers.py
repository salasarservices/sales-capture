"""Django REST Framework serializers - mirroring Pydantic models."""

from rest_framework import serializers
from .models import Enquiry, User


class EnquirySerializer(serializers.ModelSerializer):
    """Serializer for Enquiry model - mirrors EnquiryOut."""
    
    tentative_brokerage_12pct = serializers.ReadOnlyField()

    class Meta:
        model = Enquiry
        fields = [
            "id", "enquiry_no", "timestamp", "date_referred", "contact_person",
            "company_name", "phone", "email", "requirement", "premium_potential",
            "tentative_brokerage_12pct", "type_of_proposal", "expiry_date_existing_policy",
            "cre_rm_accountable", "quote_planned_date", "quote_actual_date",
            "quote_submitted", "closure_planned_date", "closure_actual_date",
            "business_closed", "reason_not_closed", "fy", "branch",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "timestamp", "created_at", "updated_at"]


class EnquiryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating enquiries - mirrors EnquiryCreate."""

    class Meta:
        model = Enquiry
        fields = [
            "enquiry_no", "date_referred", "contact_person", "company_name",
            "phone", "email", "requirement", "premium_potential",
            "type_of_proposal", "expiry_date_existing_policy", "cre_rm_accountable",
            "quote_planned_date", "quote_actual_date", "quote_submitted",
            "closure_planned_date", "closure_actual_date", "business_closed",
            "reason_not_closed", "fy", "branch",
        ]

    def create(self, validated_data):
        if validated_data.get("premium_potential"):
            validated_data["tentative_brokerage_12pct"] = round(
                float(validated_data["premium_potential"]) * 0.12, 2
            )
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = ["id", "username", "role", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "role"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login request."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for token response."""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()