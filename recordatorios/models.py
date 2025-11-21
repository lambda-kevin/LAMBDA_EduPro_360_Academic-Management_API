# recordatorios/models.py

from django.db import models
from django.conf import settings
from tareas.models import Tarea


class RecordatorioTarea(models.Model):
    TIPO_RECORDATORIO = (
        ("correo", "Correo electrónico"),
        ("whatsapp", "WhatsApp"),
        ("ambos", "Correo y WhatsApp"),
    )

    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="recordatorios")
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recordatorios")

    tipo_recordatorio = models.CharField(max_length=20, choices=TIPO_RECORDATORIO, default="correo")
    fecha_envio = models.DateTimeField(auto_now_add=True)

    enviado = models.BooleanField(default=True)  # marca si se envió correctamente

    class Meta:
        unique_together = ("tarea", "estudiante", "tipo_recordatorio")

    def __str__(self):
        return f"Recordatorio a {self.estudiante} por {self.tarea}"
