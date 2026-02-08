from django.apps import AppConfig


class ManutenzioniConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "manutenzioni"

    def ready(self):
        """Import signals when app is ready."""
        import manutenzioni.signals  # noqa: F401
