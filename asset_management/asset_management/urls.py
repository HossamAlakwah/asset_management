"""URL configuration for the asset management project."""

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, reverse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


def redirect_admin_login(request):
    login_url = reverse("login")
    next_url = request.GET.get("next") or "/admin/"
    return redirect(f"{login_url}?next={next_url}")


urlpatterns = [
    path("admin/login/", redirect_admin_login),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/v1/auth/", include("users.api_urls")),
    path("api/v1/", include("assets.api.urls")),
    path("", include("users.urls")),
]
