from django.db.models.signals import post_save
from django.dispatch import receiver
from tareas.models import Tarea
from asignaturas.models import Asignatura
from users.models import CustomUser
from django.core.mail import send_mail

@receiver(post_save, sender=Tarea)
def notificar_estudiantes(sender, instance, created, **kwargs):
    if created and instance.estado == 'activo':
        asignatura = instance.asignatura
        estudiantes = CustomUser.objects.filter(asignaturas=asignatura, rol='estudiante')
        for estudiante in estudiantes:
            send_mail(
                'Nueva tarea publicada',
                f'Se ha publicado una nueva tarea: {instance.titulo}',
                'noreply@edupro360.com',
                [estudiante.email],
                fail_silently=True,
            )
