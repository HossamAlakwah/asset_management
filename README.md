# IT Asset Management

Django REST API plus a browser UI for IT inventory: endpoints, infrastructure, servers/VMs, employees, branches and stock alerts.

This project is source-available. You may clone and run it as provided. You may not modify it. See `LICENSE`.

## Run locally

From a terminal, in the `asset_management` directory (the one that contains `manage.py`):

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy ..\.env.example .env
```

The example `.env` sets `USE_SQLITE=true`, so you do not need Postgres for local work. Generate a unique `DJANGO_SECRET_KEY` before anything other than local development.

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data
python manage.py runserver
```

Then open:

- App: http://127.0.0.1:8000/app/
- Login: http://127.0.0.1:8000/login/
- Swagger: http://127.0.0.1:8000/api/docs/
- ReDoc: http://127.0.0.1:8000/api/redoc/
- OpenAPI schema: http://127.0.0.1:8000/api/schema/
- Admin: http://127.0.0.1:8000/admin/

## Docker

From the repository root (the folder that contains `docker-compose.yml`):

```powershell
copy .env.example .env
docker compose up --build
```

Compose starts Postgres and the app at http://127.0.0.1:8000/. It forces `USE_SQLITE=false` and talks to the `db` service even if `.env` still says SQLite. Keep `DJANGO_DEBUG=true` for local Docker unless SMTP is configured.

Then in another terminal:

```powershell
docker compose run --rm web python manage.py seed_demo_data
docker compose run --rm web python manage.py createsuperuser
```

Stop with `docker compose down`. Add `-v` only if you also want to wipe the Postgres volume.

Sign in with the superuser you just created, or with the demo accounts from `seed_demo_data`:

- `demo.admin` / `demo12345` (full write access, including Users)
- `demo.user` / `demo12345` (read-only)

Give a hand-made superuser role `super_admin` in Admin if you need the Users screen (the default role on `CustomUser` is `user`, which can still read the inventory). Re-run `python manage.py seed_demo_data` any time; add `--reset` to wipe previous demo rows first.

## Optional: PostgreSQL

In `.env`:

```
USE_SQLITE=false
POSTGRES_DB=assets
POSTGRES_USER=assets
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

Create the database, then run `python manage.py migrate` again.

## API auth from Swagger or curl

```http
POST /api/v1/auth/token/
{"username": "admin", "password": "..."}
```

Use `Authorization: Bearer <access>` on later calls. Token requests must include `"otp": "123456"` after the account has enrolled 2FA at `/login/`. The HTML app never skips that step.

## Login lockout and 2FA

Authenticator enrollment is required. After password, first sign-in shows a QR code; later sign-ins ask for the 6-digit code. The public login page (and `/admin/login/`, which redirects here) also locks a username or IP after 5 failed attempts for 15 minutes. If someone loses their device:

```powershell
python manage.py disable_2fa username
```

## Email (SMTP)

Password reset and stock alerts use Django’s mail backend. With `DJANGO_DEBUG=true` and an empty `EMAIL_HOST`, messages print in the runserver terminal. For real delivery set SMTP in `.env`:

```
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=alerts@example.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Asset Control <alerts@example.com>
```

Production (`DJANGO_DEBUG=false`) refuses to start without `EMAIL_HOST` or an explicit `EMAIL_BACKEND`. Prove the path with:

```powershell
python manage.py send_test_email you@example.com
python manage.py check_stock_levels --verbose
```

## Excel

On any list page: **Template** downloads a blank workbook, **Export** downloads the current filtered list, **Import** uploads an `.xlsx` file. Related rows are matched by name/email/hostname, not database ids.

## Stock alerts

```powershell
python manage.py check_stock_levels --verbose
```

## Tests

```powershell
python manage.py test assets.tests users.tests -v 2
```

## License

Source-available. Clone and use as provided; do not edit or redistribute modified copies. See `LICENSE`.
