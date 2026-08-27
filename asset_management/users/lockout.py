from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import LoginLock

LOCKOUT_MESSAGE = "Too many failed sign-in attempts. Try again later."
INVALID_LOGIN_MESSAGE = "Invalid username or password."


def client_ip(request):
    if request is None:
        return "0.0.0.0"
    if getattr(settings, "TRUST_PROXY_HEADERS", False):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()[:45]
    return (request.META.get("REMOTE_ADDR") or "0.0.0.0")[:45]


def normalize_username(username):
    return (username or "").strip().lower()[:150]


def _keys(request, username):
    keys = [(LoginLock.KIND_IP, client_ip(request))]
    normalized = normalize_username(username)
    if normalized:
        keys.append((LoginLock.KIND_USERNAME, normalized))
    return keys


def is_locked(request, username=""):
    now = timezone.now()
    for kind, value in _keys(request, username):
        lock = LoginLock.objects.filter(kind=kind, value=value).only("locked_until").first()
        if lock and lock.locked_until and lock.locked_until > now:
            return True
    return False


def record_failure(request, username=""):
    now = timezone.now()
    window = timedelta(seconds=int(getattr(settings, "LOGIN_FAILURE_WINDOW_SECONDS", 900)))
    limit = int(getattr(settings, "LOGIN_FAILURE_LIMIT", 5))
    lock_for = timedelta(seconds=int(getattr(settings, "LOGIN_LOCKOUT_SECONDS", 900)))

    for kind, value in _keys(request, username):
        with transaction.atomic():
            lock, _created = LoginLock.objects.select_for_update().get_or_create(
                kind=kind,
                value=value,
                defaults={"failures": 0, "window_started": now},
            )
            if lock.locked_until and lock.locked_until <= now:
                lock.locked_until = None
                lock.failures = 0
                lock.window_started = now
            elif lock.window_started and now - lock.window_started > window:
                lock.failures = 0
                lock.window_started = now
                lock.locked_until = None
            lock.failures += 1
            if lock.failures >= limit:
                lock.locked_until = now + lock_for
            lock.save()


def clear_username_failures(username):
    normalized = normalize_username(username)
    if normalized:
        LoginLock.objects.filter(kind=LoginLock.KIND_USERNAME, value=normalized).delete()
