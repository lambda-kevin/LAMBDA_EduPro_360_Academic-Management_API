from django.db.models.signals import pre_save
from django.dispatch import receiver
from tareas.models import Tarea
from recordatorios.models import RecordatorioTarea

@receiver(pre_save, sender=Tarea)
def reprogramar_recordatorios(sender, instance, **kwargs):
    if not instance.pk:
        return  # tarea nueva, nada que reprogramar

    tarea_anterior = Tarea.objects.get(pk=instance.pk)
    if tarea_anterior.fecha_vencimiento != instance.fecha_vencimiento:
        # eliminar recordatorios antiguos
        RecordatorioTarea.objects.filter(tarea=instance).delete()
