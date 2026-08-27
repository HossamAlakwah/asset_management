from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import CustomPasswordResetForm, LockedAuthenticationForm
from .lockout import LOCKOUT_MESSAGE, clear_username_failures, client_ip, is_locked, record_failure
from .twofactor import (
    confirm_setup,
    ensure_setup,
    provisioning_uri,
    qr_svg,
    two_factor_is_confirmed,
    verify_user_otp,
)

User = get_user_model()

PENDING_USER = "pending_2fa_user_id"
PENDING_BACKEND = "pending_2fa_backend"
PENDING_NEXT = "pending_2fa_next"
PENDING_KIND = "pending_2fa_kind"
PENDING_BACKUP = "pending_2fa_backup"


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("app")
        return redirect("login")


class AppLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    authentication_form = LockedAuthenticationForm

    def get(self, request, *args, **kwargs):
        if request.GET.get("cancel"):
            _clear_pending(request)
            return redirect("login")
        pending = _pending_user(request)
        if pending:
            return render(request, self.template_name, _pending_context(request, pending))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get("otp_step"):
            return self._verify_otp(request)
        if request.POST.get("setup_step"):
            return self._confirm_setup(request)
        if request.POST.get("setup_continue"):
            return self._finish_pending_login(request)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        request = self.request
        request.session[PENDING_USER] = user.pk
        request.session[PENDING_BACKEND] = getattr(user, "backend", "")
        request.session[PENDING_NEXT] = self.get_success_url()
        clear_username_failures(user.username)
        if two_factor_is_confirmed(user):
            request.session[PENDING_KIND] = "otp"
            return render(request, self.template_name, {"otp_step": True})
        request.session[PENDING_KIND] = "setup"
        return render(request, self.template_name, _setup_context(user))

    def _verify_otp(self, request):
        user = _pending_user(request)
        if user is None:
            return redirect("login")
        if is_locked(request, user.username):
            return render(
                request,
                self.template_name,
                {"otp_step": True, "otp_error": LOCKOUT_MESSAGE},
            )
        code = (request.POST.get("otp") or "").strip()
        if not verify_user_otp(user, code):
            record_failure(request, user.username)
            message = (
                LOCKOUT_MESSAGE
                if is_locked(request, user.username)
                else "Invalid or expired authentication code."
            )
            return render(
                request,
                self.template_name,
                {"otp_step": True, "otp_error": message},
            )
        return self._finish_pending_login(request)

    def _confirm_setup(self, request):
        user = _pending_user(request)
        if user is None:
            return redirect("login")
        codes = confirm_setup(user, (request.POST.get("otp") or "").strip())
        if codes is None:
            return render(
                request,
                self.template_name,
                {**_setup_context(user), "otp_error": "Invalid or expired authentication code."},
            )
        request.session[PENDING_KIND] = "backup"
        request.session[PENDING_BACKUP] = codes
        return render(request, self.template_name, {"backup_codes": codes})

    def _finish_pending_login(self, request):
        user = _pending_user(request)
        if user is None or not two_factor_is_confirmed(user):
            _clear_pending(request)
            return redirect("login")
        backend = request.session.get(PENDING_BACKEND) or None
        next_url = request.session.get(PENDING_NEXT) or self.get_success_url()
        _clear_pending(request)
        login(request, user, backend=backend)
        request.session["two_factor_verified"] = True
        return redirect(next_url)


def _pending_user(request):
    user_id = request.session.get(PENDING_USER)
    if not user_id:
        return None
    return User.objects.filter(pk=user_id).first()


def _setup_context(user, extra=None):
    device = ensure_setup(user)
    uri = provisioning_uri(user, device)
    context = {
        "setup_step": True,
        "qr_svg": qr_svg(uri),
        "secret": device.secret,
    }
    if extra:
        context.update(extra)
    return context


def _pending_context(request, user):
    kind = request.session.get(PENDING_KIND)
    if kind == "backup":
        return {"backup_codes": request.session.get(PENDING_BACKUP) or []}
    if kind == "setup":
        return _setup_context(user)
    return {"otp_step": True}


def _clear_pending(request):
    for key in (PENDING_USER, PENDING_BACKEND, PENDING_NEXT, PENDING_KIND, PENDING_BACKUP):
        request.session.pop(key, None)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        ip = client_ip(self.request)
        cache_key = f"pwdreset:{ip}"
        attempts = cache.get(cache_key, 0)
        if attempts >= 8:
            return redirect(self.success_url)
        cache.set(cache_key, attempts + 1, 3600)
        return super().form_valid(form)
