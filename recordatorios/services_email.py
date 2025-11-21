from django.core.mail import send_mail
from django.conf import settings

def enviar_recordatorio_email(estudiante, tarea):
    asunto = f"Recordatorio: La tarea '{tarea.titulo}' vence pronto"
    mensaje = (
        f"Hola {estudiante.nombre},\n\n"
        f"La tarea '{tarea.titulo}' vence el {tarea.fecha_vencimiento}.\n"
        "No olvides subir tu entrega.\n\n"
        "Saludos,\nEquipo Académico"
    )

    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [estudiante.correo],
        fail_silently=False,
    )
