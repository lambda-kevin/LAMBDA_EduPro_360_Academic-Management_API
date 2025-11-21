from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from tareas.models import Tarea
from entrega_tareas.models import EntregaTarea
from users.models import CustomUser

from recordatorios.models import RecordatorioTarea
from recordatorios.services_email import enviar_recordatorio_email


@shared_task
def enviar_recordatorios_tareas():
    hoy = timezone.now().date()
    fecha_limite = hoy + timedelta(days=1)

    tareas = Tarea.objects.filter(fecha_vencimiento=fecha_limite)
    estudiantes = CustomUser.objects.filter(rol="estudiante", is_active=True)

    total = 0

    for tarea in tareas:
        for estudiante in estudiantes:

            if EntregaTarea.objects.filter(tarea=tarea, estudiante=estudiante).exists():
                continue

            if RecordatorioTarea.objects.filter(estudiante=estudiante, tarea=tarea).exists():
                continue

            enviar_recordatorio_email(estudiante, tarea)

            RecordatorioTarea.objects.create(estudiante=estudiante, tarea=tarea)
            total += 1

    return f"{total} notificaciones enviadas"
