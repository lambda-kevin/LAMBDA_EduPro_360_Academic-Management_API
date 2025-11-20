from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CalificacionEntrega, NotaFinalAsignatura
from tareas.models import Tarea
from entrega_tareas.models import EntregaTarea


@receiver(post_save, sender=CalificacionEntrega)
def recalcular_nota_final(sender, instance, **kwargs):
    entrega = instance.entrega
    estudiante = entrega.estudiante
    asignatura = entrega.tarea.asignatura

    # Todas las ENTREGAS con calificación
    entregas = EntregaTarea.objects.filter(
        estudiante=estudiante,
        tarea__asignatura=asignatura,
        calificacion__isnull=False
    )

    nota_final = 0

    for e in entregas:
        tarea = e.tarea
        peso = tarea.peso_porcentual / 100
        nota_final += float(e.calificacion.nota) * peso

    nota_obj, _ = NotaFinalAsignatura.objects.get_or_create(
        estudiante=estudiante,
        asignatura=asignatura
    )

    nota_obj.nota_final = round(nota_final, 2)
    nota_obj.save()
