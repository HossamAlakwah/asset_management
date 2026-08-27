import io
import secrets

import pyotp
import qrcode
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from qrcode.image.svg import SvgPathImage

from .models import TwoFactorDevice


def two_factor_is_confirmed(user):
    if not user or not getattr(user, "pk", None):
        return False
    try:
        return bool(user.totp_device.confirmed)
    except TwoFactorDevice.DoesNotExist:
        return False


def issuer_name():
    return getattr(settings, "OTP_ISSUER", "Asset Control")


def ensure_setup(user):
    """Reuse an unconfirmed secret so the login QR does not rotate on refresh."""
    device = TwoFactorDevice.objects.filter(user=user).first()
    if device:
        return device
    return TwoFactorDevice.objects.create(
        user=user,
        secret=pyotp.random_base32(),
        confirmed=False,
    )


def start_setup(user):
    secret = pyotp.random_base32()
    device, created = TwoFactorDevice.objects.get_or_create(
        user=user,
        defaults={"secret": secret, "confirmed": False},
    )
    if device.confirmed:
        return device
    if not created:
        device.secret = secret
        device.backup_hashes = []
        device.save(update_fields=["secret", "backup_hashes"])
    return device


def provisioning_uri(user, device):
    totp = pyotp.TOTP(device.secret)
    account = user.email or user.username
    return totp.provisioning_uri(name=account, issuer_name=issuer_name())


def qr_svg(uri):
    image = qrcode.make(uri, image_factory=SvgPathImage, box_size=6)
    buffer = io.BytesIO()
    image.save(buffer)
    return buffer.getvalue().decode("utf-8")


def generate_backup_codes(count=8):
    codes = []
    for _ in range(count):
        raw = secrets.token_hex(4).upper()
        codes.append(f"{raw[:4]}-{raw[4:]}")
    return codes


def confirm_setup(user, code):
    try:
        device = user.totp_device
    except TwoFactorDevice.DoesNotExist:
        return None
    if device.confirmed:
        return None
    if not pyotp.TOTP(device.secret).verify(_digits(code), valid_window=1):
        return None
    codes = generate_backup_codes()
    device.backup_hashes = [make_password(item) for item in codes]
    device.confirmed = True
    device.confirmed_at = timezone.now()
    device.save(update_fields=["backup_hashes", "confirmed", "confirmed_at"])
    return codes


def _digits(code):
    return "".join(ch for ch in (code or "") if ch.isdigit())


def canonical_backup(code):
    compact = "".join(ch for ch in (code or "") if ch.isalnum()).upper()
    if len(compact) != 8:
        return None
    return f"{compact[:4]}-{compact[4:]}"


def verify_user_otp(user, code):
    try:
        device = user.totp_device
    except TwoFactorDevice.DoesNotExist:
        return False
    if not device.confirmed:
        return False
    digits = _digits(code)
    if len(digits) == 6 and pyotp.TOTP(device.secret).verify(digits, valid_window=1):
        return True
    backup = canonical_backup(code)
    if not backup:
        return False
    hashes = list(device.backup_hashes or [])
    for index, hashed in enumerate(hashes):
        if check_password(backup, hashed):
            hashes.pop(index)
            device.backup_hashes = hashes
            device.save(update_fields=["backup_hashes"])
            return True
    return False


def disable_two_factor(user):
    TwoFactorDevice.objects.filter(user=user).delete()
