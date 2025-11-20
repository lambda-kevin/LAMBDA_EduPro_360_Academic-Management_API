from django.db.models.signals import post_save
from django.dispatch import receiver
from entrega_tareas.models import EntregaTarea
from tareas.models import Tarea
from users.models import CustomUser
from django.core.mail import send_mail

@receiver(post_save, sender=EntregaTarea)
def notificar_docente(sender, instance, created, **kwargs):
    if created:
        tarea = instance.tarea
        docente = tarea.asignatura.docente  # Suponiendo que Asignatura tiene un campo docente
        send_mail(
            'Nueva entrega registrada',
            f'El estudiante {instance.estudiante} ha subido una entrega para la tarea: {tarea.titulo}',
            'noreply@edupro360.com',
            [docente.email],
            fail_silently=True,
        )
