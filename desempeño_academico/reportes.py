# recordatorios/reportes.py

from datetime import datetime, date
from calendar import monthrange
from django.db.models import Avg, Count, Q, F
from django.conf import settings

from asignaturas.models import Asignatura
from tareas.models import Tarea
from entrega_tareas.models import EntregaTarea
from calificaciones.models import CalificacionEntrega, NotaFinalAsignatura
from users.models import CustomUser, Rol, Permiso, UsuarioRol

# Umbral para considerar aprobada una nota (ajusta si tu escala es 0-5 o 0-100)
NOTA_APROBACION = getattr(settings, "NOTA_APROBACION", 3.0)


def periodo_mes_anterior(ref_date: date = None):
    """ Retorna (anio, mes, fecha_inicio, fecha_fin) del mes anterior al ref_date.
        Si no se pasa ref_date, usa hoy()."""
    hoy = ref_date or date.today()
    año = hoy.year
    mes = hoy.month - 1
    if mes == 0:
        mes = 12
        año -= 1
    inicio = date(año, mes, 1)
    fin = date(año, mes, monthrange(año, mes)[1])
    return año, mes, inicio, fin


def obtener_usuarios_con_permiso(nombre_permiso="recibir_notificacion_estado_mensual"):
    """Devuelve queryset de usuarios que tengan el permiso por tu sistema de roles/permisos."""
    # Buscar permisos con ese nombre
    permisos = Permiso.objects.filter(nombre=nombre_permiso)
    if not permisos.exists():
        return CustomUser.objects.none()

    # Usuarios que tienen roles que contienen ese permiso
    usuarios_ids = UsuarioRol.objects.filter(
        rol__permisos__in=permisos
    ).values_list("usuario_id", flat=True).distinct()

    return CustomUser.objects.filter(id__in=usuarios_ids, is_active=True)


def calcular_metrica_por_asignatura(fecha_inicio: date, fecha_fin: date):
    """
    Genera métricas por asignatura entre fecha_inicio y fecha_fin.
    Retorna una lista de dicts con:
      periodo, asignatura_id, asignatura_nombre, total_estudiantes,
      promedio_general, tasa_aprobacion, tareas_pendientes
    """
    resultado = []

    asignaturas = Asignatura.objects.all()

    for a in asignaturas:
        # 1) Total estudiantes: consideramos alumnos que tienen alguna nota final en la asignatura
        estudiantes_qs = CustomUser.objects.filter(
            notas_finales__asignatura=a
        ).distinct()

        total_estudiantes = estudiantes_qs.count()

        # 2) Promedio general: promedio de notas finales en la asignatura dentro del periodo
        notas_qs = NotaFinalAsignatura.objects.filter(
            asignatura=a,
            # asumo que NotaFinalAsignatura no tiene fecha; si la guardas por mes, filtrar por fecha_generacion
        )

        # Si guardas notas por mes, filtra por fecha; si no, calcularemos desde CalificacionEntrega por el periodo:
        promedio_general = None
        # Intentamos calcular promediando calificaciones entregadas en el periodo por la asignatura
        califs = CalificacionEntrega.objects.filter(
            entrega__tarea__asignatura=a,
            fecha_calificacion__date__gte=fecha_inicio,
            fecha_calificacion__date__lte=fecha_fin,
            estado_calificacion="publicado"
        ).aggregate(promedio=Avg("nota"))
        promedio_general = round(califs["promedio"] or 0, 2) if califs["promedio"] is not None else None

        # 3) Tasa de aprobación: porcentaje de calificaciones >= NOTA_APROBACION sobre total calificaciones publicadas
        total_pub = CalificacionEntrega.objects.filter(
            entrega__tarea__asignatura=a,
            fecha_calificacion__date__gte=fecha_inicio,
            fecha_calificacion__date__lte=fecha_fin,
            estado_calificacion="publicado"
        ).count()

        tot_aprobadas = CalificacionEntrega.objects.filter(
            entrega__tarea__asignatura=a,
            fecha_calificacion__date__gte=fecha_inicio,
            fecha_calificacion__date__lte=fecha_fin,
            estado_calificacion="publicado",
            nota__gte=NOTA_APROBACION
        ).count()

        tasa_aprobacion = round((tot_aprobadas / total_pub) * 100, 2) if total_pub > 0 else None

        # 4) Tareas pendientes: contamos tareas del periodo en la asignatura que tienen entregas faltantes por estudiante.
        # Para simplificar, contamos tareas activas publicadas en el periodo sin entregas (a nivel tarea).
        tareas_periodo = Tarea.objects.filter(
            asignatura=a,
            fecha_publicacion__gte=fecha_inicio,
            fecha_publicacion__lte=fecha_fin
        )

        tareas_pendientes = 0
        for t in tareas_periodo:
            # Si ninguna entrega registrada => pendiente (puedes mejorar por estudiantes inscritos)
            if not EntregaTarea.objects.filter(tarea=t).exists():
                tareas_pendientes += 1

        resultado.append({
            "asignatura_id": a.id,
            "asignatura_nombre": a.nombre,
            "periodo": f"{fecha_inicio.strftime('%Y-%m-%d')} a {fecha_fin.strftime('%Y-%m-%d')}",
            "total_estudiantes": total_estudiantes,
            "promedio_general": promedio_general,
            "tasa_aprobacion": tasa_aprobacion,
            "tareas_pendientes": tareas_pendientes
        })

    return resultado


def resumen_global(metrica_asignaturas):
    """A partir de la lista por asignatura genera:
       asignaturas_con_mayor_reprobacion y docentes_con_mejor_promedio"""
    # 1) Asignaturas con mayor reprobación: orden por (100 - tasa_aprobacion) o por tasa reprobación
    asignaturas_reprob = sorted(
        [m for m in metrica_asignaturas if m["tasa_aprobacion"] is not None],
        key=lambda x: (100 - x["tasa_aprobacion"]),
        reverse=True
    )[:5]  # top 5

    # 2) Docentes con mejor promedio: asumimos Asignatura tiene campo docente_responsable si existe
    docentes_prom = {}
    for m in metrica_asignaturas:
        # tratamos que cada asignatura pueda tener docente_responsable
        try:
            a = Asignatura.objects.get(id=m["asignatura_id"])
            docente = getattr(a, "docente_responsable", None)
            if docente:
                docentes_prom.setdefault(docente.id, {"docente": docente, "acum": 0, "count": 0})
                if m["promedio_general"]:
                    docentes_prom[docente.id]["acum"] += m["promedio_general"]
                    docentes_prom[docente.id]["count"] += 1
        except Asignatura.DoesNotExist:
            continue

    docentes_list = []
    for v in docentes_prom.values():
        avg = round(v["acum"] / v["count"], 2) if v["count"] > 0 else None
        docentes_list.append({
            "docente_id": v["docente"].id,
            "docente_nombre": str(v["docente"]),
            "promedio": avg
        })

    docentes_list = sorted([d for d in docentes_list if d["promedio"] is not None], key=lambda x: x["promedio"], reverse=True)[:5]

    return {
        "asignaturas_con_mayor_reprobacion": asignaturas_reprob,
        "docentes_con_mejor_promedio": docentes_list
    }
