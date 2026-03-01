"""
weltenfw.django.app_config - Django AppConfig + get_client()

get_client() liefert einen WeltenClient pro Django-Worker-Prozess (lazy init).
Nur fuer Single-Tenant-Apps geeignet. Multi-Tenant-Konsumenten instanziieren
pro Request einen eigenen WeltenClient mit dem jeweiligen User-Token.

Konfiguration in settings.py:
    WELTENHUB_URL         = "https://weltenforger.com/api/v1"
    WELTENHUB_TOKEN       = env("WELTENHUB_TOKEN")
    WELTENHUB_LOOKUP_TTL  = 3600  # Sekunden (optional)
    WELTENHUB_TIMEOUT     = 30.0  # HTTP-Timeout (optional)

Installed Apps:
    INSTALLED_APPS = [..., "weltenfw.django"]
"""

from __future__ import annotations

from django.apps import AppConfig

_client_instance = None


class WeltenfwConfig(AppConfig):
    name = "weltenfw.django"
    label = "weltenfw"
    verbose_name = "WeltenHub Client Framework"

    def ready(self) -> None:
        pass


default_app_config = "weltenfw.django.app_config.WeltenfwConfig"


def get_client():
    """Gibt den WeltenClient fuer diesen Worker-Prozess zurueck (lazy init).

    WARNUNG: Nur fuer Single-Tenant-Apps. Multi-Tenant-Konsumenten
    erstellen pro Tenant-Request einen eigenen WeltenClient.

    Token-Rotation erfordert Container-Restart (kein Hot-Reload in v1).

    Returns:
        WeltenClient mit DjangoCache fuer Lookups.

    Raises:
        ImproperlyConfigured: Wenn WELTENHUB_URL oder WELTENHUB_TOKEN fehlen.
    """
    global _client_instance
    if _client_instance is None:
        from django.conf import settings
        from django.core.exceptions import ImproperlyConfigured

        from weltenfw.client import WeltenClient
        from weltenfw.django.cache import DjangoCache

        url = getattr(settings, "WELTENHUB_URL", None)
        token = getattr(settings, "WELTENHUB_TOKEN", None)

        if not url:
            raise ImproperlyConfigured(
                "WELTENHUB_URL is required in settings. "
                "Example: WELTENHUB_URL = 'https://weltenforger.com/api/v1'"
            )
        if not token:
            raise ImproperlyConfigured(
                "WELTENHUB_TOKEN is required in settings. "
                "Set via: WELTENHUB_TOKEN = env('WELTENHUB_TOKEN')"
            )

        ttl = getattr(settings, "WELTENHUB_LOOKUP_TTL", 3600)
        timeout = getattr(settings, "WELTENHUB_TIMEOUT", 30.0)

        _client_instance = WeltenClient(
            base_url=url,
            token=token,
            lookup_cache=DjangoCache(alias="default", ttl=ttl),
            lookup_ttl=ttl,
            timeout=timeout,
        )
    return _client_instance


def reset_client() -> None:
    """Setzt den Singleton zurueck. Nur fuer Tests."""
    global _client_instance
    _client_instance = None
