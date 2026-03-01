"""
weltenfw.django - Optionale Django-Integration

Nur verfuegbar mit: pip install weltenfw[django]

Public API:
    from weltenfw.django import get_client
    client = get_client()  # lazy, per Worker
"""

from weltenfw.django.app_config import get_client, reset_client

__all__ = ["get_client", "reset_client"]
