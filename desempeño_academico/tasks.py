# recordatorios/tasks.py

from celery import shared_task
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings

from .reportes import periodo_mes_anterior, calcular_metrica_por_asignatura, resumen_global, obtener_usuarios_con_permiso
from .pdf_report import generar_pdf_reporte

@shared_task(bind=True)
def generar_reporte_mensual(self, anio=None, mes=None):
    """
    Genera el consolidado del mes anterior por defecto.
    Puedes forzar con (anio, mes) -> ints.
    """
    # Determinar periodo si no viene: mes anterior respecto a hoy
    if anio is None or mes is None:
        año, mes_calc, inicio, fin = periodo_mes_anterior()
    else:
        año = int(anio)
        mes_calc = int(mes)
        inicio = timezone.datetime(año, mes_calc, 1).date()
        fin = timezone.datetime(año, mes_calc, monthrange(año, mes_calc)[1]).date()

    # Calcular métricas
    metricas = calcular_metrica_por_asignatura(inicio, fin)
    resumen = resumen_global(metricas)

    fecha_generacion = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    mes_año_str = f"{mes_calc}/{año}"

    # Generar PDF
    pdf_buffer = generar_pdf_reporte(mes_año_str, metricas, resumen, fecha_generacion=fecha_generacion)

    # Buscar usuarios con permiso
    usuarios = obtener_usuarios_con_permiso("recibir_notificacion_estado_mensual")

    # Si no hay usuarios, terminar pero devolver resumen
    if not usuarios.exists():
        return {
            "status": "no_receptores",
            "mensaje": "No se encontraron usuarios con permiso recibir_notificacion_estado_mensual",
            "total_asignaturas": len(metricas)
        }

    # Enviar correo con adjunto a cada usuario
    remitente = getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER)

    enviados = 0
    for u in usuarios:
        try:
            email = EmailMessage(
                subject=f"Reporte mensual académico {mes_año_str}",
                body=f"Adjunto encontrarás el reporte consolidado del periodo {mes_año_str}.",
                from_email=remitente,
                to=[u.correo],
            )
            # Adjuntar PDF
            email.attach(f"consolidado_{mes_calc}_{año}.pdf", pdf_buffer.getvalue(), "application/pdf")
            email.send(fail_silently=False)
            enviados += 1
        except Exception as e:
            # registrar errores en logs si quieres
            continue

    return {
        "status": "ok",
        "mensaje": f"Reporte generado y enviado a {enviados} usuarios.",
        "total_asignaturas": len(metricas)
    }
