from django.apps import AppConfig

class RecordatoriosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recordatorios"

    def ready(self):
        import recordatorios.signals  # conecta los signals
