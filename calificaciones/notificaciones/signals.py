from django.db.models.signals import post_save
from django.dispatch import receiver
from calificaciones.models import CalificacionEntrega
from .models import Notificacion


@receiver(post_save, sender=CalificacionEntrega)
def notificar_estudiante(sender, instance, **kwargs):
    if instance.estado_calificacion == "publicado":
        estudiante = instance.entrega.estudiante
        tarea = instance.entrega.tarea

        Notificacion.objects.create(
            usuario=estudiante,
            mensaje=f"Tu calificación para '{tarea.titulo}' ha sido publicada: {instance.nota}"
        )
