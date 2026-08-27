from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .lockout import (
    LOCKOUT_MESSAGE,
    clear_username_failures,
    is_locked,
    record_failure,
)
from .twofactor import two_factor_is_confirmed, verify_user_otp

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    two_factor_enabled = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "is_active",
            "two_factor_enabled",
        )
        read_only_fields = ("id", "two_factor_enabled")

    def get_two_factor_enabled(self, user):
        return two_factor_is_confirmed(user)


class LockedTokenObtainPairSerializer(TokenObtainPairSerializer):
    otp = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
        help_text="Authenticator or backup code (required).",
    )

    def validate(self, attrs):
        otp = attrs.pop("otp", "") or ""
        request = self.context.get("request")
        username = attrs.get(self.username_field) or ""
        if request and is_locked(request, username):
            raise AuthenticationFailed(LOCKOUT_MESSAGE)
        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            if request:
                record_failure(request, username)
                if is_locked(request, username):
                    raise AuthenticationFailed(LOCKOUT_MESSAGE) from None
            raise
        user = self.user
        if not two_factor_is_confirmed(user):
            raise AuthenticationFailed(
                "Two-factor authentication must be enrolled at /login/ before API tokens can be issued."
            )
        if not str(otp).strip():
            raise AuthenticationFailed("Two-factor authentication code required.")
        if not verify_user_otp(user, otp):
            if request:
                record_failure(request, username)
                if is_locked(request, username):
                    raise AuthenticationFailed(LOCKOUT_MESSAGE)
            raise AuthenticationFailed("Invalid authentication code.")
        if request:
            clear_username_failures(username)
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "phone",
            "is_active",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
