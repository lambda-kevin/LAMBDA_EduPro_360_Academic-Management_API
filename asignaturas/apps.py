from django.apps import AppConfig


class AsignaturasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'asignaturas'

    def ready(self):
        import asignaturas.signals
