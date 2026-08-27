"""Login lockout, required TOTP 2FA, and JWT otp checks."""

import pyotp
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from users.models import LoginLock
from users.twofactor import confirm_setup, start_setup

User = get_user_model()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    LOGIN_FAILURE_LIMIT=3,
    LOGIN_LOCKOUT_SECONDS=900,
    LOGIN_FAILURE_WINDOW_SECONDS=900,
)
class AuthSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="lock.user",
            password="lock-pass-123",
            email="lock.user@example.com",
            role="admin",
        )
        self.api = APIClient()

    def test_failed_logins_lock_even_the_correct_password(self):
        for _ in range(3):
            response = self.client.post(
                "/login/",
                {"username": "lock.user", "password": "wrong"},
            )
            self.assertEqual(response.status_code, 200)
        locked = self.client.post(
            "/login/",
            {"username": "lock.user", "password": "lock-pass-123"},
        )
        self.assertEqual(locked.status_code, 200)
        self.assertContains(locked, "Too many failed")
        self.assertFalse(locked.wsgi_request.user.is_authenticated)

    def test_successful_password_clears_lock_but_requires_setup(self):
        self.client.post("/login/", {"username": "lock.user", "password": "wrong"})
        ok = self.client.post(
            "/login/",
            {"username": "lock.user", "password": "lock-pass-123"},
        )
        self.assertEqual(ok.status_code, 200)
        self.assertContains(ok, "setup_step")
        self.assertContains(ok, "Authenticator is required")
        self.assertFalse(ok.wsgi_request.user.is_authenticated)
        self.assertFalse(LoginLock.objects.filter(kind="username", value="lock.user").exists())

    def test_first_login_enrolls_2fa_then_opens_app(self):
        password_ok = self.client.post(
            "/login/",
            {"username": "lock.user", "password": "lock-pass-123"},
        )
        self.assertEqual(password_ok.status_code, 200)
        self.assertContains(password_ok, "setup_step")
        secret = password_ok.context["secret"]
        confirm = self.client.post(
            "/login/",
            {"setup_step": "1", "otp": pyotp.TOTP(secret).now()},
        )
        self.assertEqual(confirm.status_code, 200)
        self.assertEqual(len(confirm.context["backup_codes"]), 8)
        done = self.client.post("/login/", {"setup_continue": "1"})
        self.assertEqual(done.status_code, 302)
        app = self.client.get("/app/")
        self.assertEqual(app.status_code, 200)

    def test_login_then_totp_then_app(self):
        device = start_setup(self.user)
        codes = confirm_setup(self.user, pyotp.TOTP(device.secret).now())
        self.assertTrue(codes)
        password_ok = self.client.post(
            "/login/",
            {"username": "lock.user", "password": "lock-pass-123"},
        )
        self.assertEqual(password_ok.status_code, 200)
        self.assertContains(password_ok, "otp_step")
        self.assertFalse(password_ok.wsgi_request.user.is_authenticated)
        otp_ok = self.client.post(
            "/login/",
            {"otp_step": "1", "otp": pyotp.TOTP(self.user.totp_device.secret).now()},
        )
        self.assertEqual(otp_ok.status_code, 302)
        app = self.client.get("/app/")
        self.assertEqual(app.status_code, 200)

    def test_successful_otp_clears_failed_otp_attempts(self):
        device = start_setup(self.user)
        confirm_setup(self.user, pyotp.TOTP(device.secret).now())
        password_ok = self.client.post(
            "/login/",
            {"username": "lock.user", "password": "lock-pass-123"},
        )
        self.assertContains(password_ok, "otp_step")
        failed = self.client.post("/login/", {"otp_step": "1", "otp": "000000"})
        self.assertEqual(failed.status_code, 200)
        self.assertTrue(
            LoginLock.objects.filter(kind="username", value="lock.user").exists()
        )
        otp_ok = self.client.post(
            "/login/",
            {"otp_step": "1", "otp": pyotp.TOTP(self.user.totp_device.secret).now()},
        )
        self.assertEqual(otp_ok.status_code, 302)
        self.assertFalse(
            LoginLock.objects.filter(kind="username", value="lock.user").exists()
        )

    def test_jwt_refuses_token_until_2fa_is_enrolled(self):
        denied = self.api.post(
            "/api/v1/auth/token/",
            {"username": "lock.user", "password": "lock-pass-123"},
            format="json",
        )
        self.assertEqual(denied.status_code, 401)

    def test_jwt_requires_otp_when_2fa_is_on(self):
        device = start_setup(self.user)
        confirm_setup(self.user, pyotp.TOTP(device.secret).now())
        denied = self.api.post(
            "/api/v1/auth/token/",
            {"username": "lock.user", "password": "lock-pass-123"},
            format="json",
        )
        self.assertEqual(denied.status_code, 401)
        allowed = self.api.post(
            "/api/v1/auth/token/",
            {
                "username": "lock.user",
                "password": "lock-pass-123",
                "otp": pyotp.TOTP(self.user.totp_device.secret).now(),
            },
            format="json",
        )
        self.assertEqual(allowed.status_code, 200, allowed.data)
        self.assertIn("access", allowed.data)

    def test_backup_code_works_once(self):
        device = start_setup(self.user)
        backup = confirm_setup(self.user, pyotp.TOTP(device.secret).now())
        first = self.api.post(
            "/api/v1/auth/token/",
            {
                "username": "lock.user",
                "password": "lock-pass-123",
                "otp": backup[0],
            },
            format="json",
        )
        self.assertEqual(first.status_code, 200, first.data)
        second = self.api.post(
            "/api/v1/auth/token/",
            {
                "username": "lock.user",
                "password": "lock-pass-123",
                "otp": backup[0],
            },
            format="json",
        )
        self.assertEqual(second.status_code, 401)

    def test_password_reset_uses_mail_backend(self):
        sent = self.client.post("/password_reset/", {"email": "lock.user@example.com"})
        self.assertEqual(sent.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("reset", mail.outbox[0].subject.lower())

    def test_admin_login_redirects_to_app_login(self):
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])
