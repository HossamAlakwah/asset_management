from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

from .twofactor import two_factor_is_confirmed

EXEMPT_PREFIXES = (
    "/login/",
    "/logout/",
    "/password_reset/",
    "/reset/",
    "/static/",
)


class TwoFactorMiddleware:
    """Session users cannot use the app until 2FA is enrolled and verified."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if (
            user is not None
            and user.is_authenticated
            and not _is_exempt(request.path)
            and (
                not two_factor_is_confirmed(user)
                or not request.session.get("two_factor_verified")
            )
        ):
            logout(request)
            login_url = reverse("login")
            if request.path != login_url:
                return redirect(f"{login_url}?next={request.path}")
            return redirect(login_url)
        return self.get_response(request)


def _is_exempt(path):
    return any(path.startswith(prefix) for prefix in EXEMPT_PREFIXES)
