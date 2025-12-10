import os
from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError


class SmashpointappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smashpointApp'

    def ready(self):
        self._ensure_default_superuser()

    def _ensure_default_superuser(self):
        """Create a default superuser if none exists (use env vars when provided)."""
        username = os.getenv('ADMIN_USER', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        password = os.getenv('ADMIN_PASSWORD', 'Admin123!')

        try:
            User = get_user_model()
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
        except (OperationalError, ProgrammingError):
            # DB not ready (migrations), skip without failing app startup.
            return
        except Exception:
            # Any other error (e.g., concurrency) is ignored to avoid breaking startup.
            return
