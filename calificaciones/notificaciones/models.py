from django.db import models
from users.models import CustomUser

class Notificacion(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificación para {self.usuario}"
