from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import LockedTokenObtainPairView, MeAPIView, TwoFactorStatusView

urlpatterns = [
    path("token/", LockedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("2fa/", TwoFactorStatusView.as_view(), name="two_factor_status"),
]
