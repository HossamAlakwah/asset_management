"""Wait for Postgres, migrate, then run the container command."""

import os
import socket
import subprocess
import sys
import time


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


def wait_for_postgres():
    if env_bool("USE_SQLITE", False):
        return
    host = os.environ.get("POSTGRES_HOST", "db")
    port = int(os.environ.get("POSTGRES_PORT", "5432"))
    for _ in range(60):
        try:
            with socket.create_connection((host, port), timeout=2):
                return
        except OSError:
            time.sleep(1)
    sys.exit(f"Postgres at {host}:{port} did not become ready.")


def manage(*args):
    subprocess.check_call([sys.executable, "manage.py", *args])


def main():
    wait_for_postgres()
    extra = sys.argv[1:]
    if extra and extra[0] != "gunicorn":
        manage("migrate", "--noinput")
        os.execvp(extra[0], extra)
    manage("migrate", "--noinput")
    manage("collectstatic", "--noinput")
    command = extra or [
        "gunicorn",
        "asset_management.wsgi:application",
        "--bind",
        "0.0.0.0:8000",
        "--workers",
        os.environ.get("GUNICORN_WORKERS", "3"),
        "--access-logfile",
        "-",
        "--error-logfile",
        "-",
    ]
    os.execvp(command[0], command)


if __name__ == "__main__":
    main()
