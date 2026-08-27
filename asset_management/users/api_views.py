from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsSuperAdmin
from .serializers import (
    LockedTokenObtainPairSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from .twofactor import two_factor_is_confirmed

User = get_user_model()


class LockedTokenObtainPairView(TokenObtainPairView):
    serializer_class = LockedTokenObtainPairSerializer


@extend_schema(
    tags=["Auth"],
    summary="Current user",
    description="Profile and role of the authenticated caller.",
    responses={200: UserSerializer},
)
class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


@extend_schema(
    tags=["Auth"],
    summary="Two-factor status",
    responses={
        200: inline_serializer(
            "TwoFactorStatus",
            fields={"enabled": serializers.BooleanField()},
        )
    },
)
class TwoFactorStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"enabled": two_factor_is_confirmed(request.user)})


@extend_schema_view(
    list=extend_schema(summary="List users"),
    create=extend_schema(summary="Create a user"),
    retrieve=extend_schema(summary="Retrieve a user"),
    update=extend_schema(summary="Replace a user"),
    partial_update=extend_schema(summary="Update a user"),
    destroy=extend_schema(summary="Delete a user"),
)
@extend_schema(description="Restricted to the `super_admin` role.")
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("totp_device").order_by("username")
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]
    search_fields = ["username", "email", "first_name", "last_name"]
    filterset_fields = ["role", "is_active"]
    ordering_fields = ["username", "email", "role"]

    ui_title = "Users"
    ui_group = "Administration"
    ui_icon = "shield"
    ui_list_fields = ["username", "full_name", "email", "role", "is_active"]
    ui_option_fields = ["username"]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer
