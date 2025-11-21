# recordatorios/pdf_report.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
import locale

locale.setlocale(locale.LC_TIME, "")  # para nombres de mes locales

def generar_pdf_reporte(mes_año_str, metricas_por_asignatura, resumen_global, fecha_generacion=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []

    # Título
    story.append(Paragraph(f"Consolidado Mensual - {mes_año_str}", styles['Title']))
    story.append(Spacer(1, 12))

    if fecha_generacion:
        story.append(Paragraph(f"Fecha generación: {fecha_generacion}", styles['Normal']))
        story.append(Spacer(1, 12))

    # Tabla por asignatura
    story.append(Paragraph("Métricas por asignatura", styles['Heading2']))
    story.append(Spacer(1, 6))

    data = [["Asignatura", "Total Estudiantes", "Promedio", "Tasa Aprobación (%)", "Tareas Pendientes"]]
    for m in metricas_por_asignatura:
        data.append([
            m["asignatura_nombre"],
            m["total_estudiantes"] if m["total_estudiantes"] is not None else "-",
            m["promedio_general"] if m["promedio_general"] is not None else "-",
            m["tasa_aprobacion"] if m["tasa_aprobacion"] is not None else "-",
            m["tareas_pendientes"]
        ])

    table = Table(data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
    ]))
    story.append(table)
    story.append(Spacer(1, 14))

    # Asignaturas con mayor reprobación
    story.append(Paragraph("Asignaturas con mayor reprobación (Top)", styles['Heading2']))
    for ar in resumen_global.get("asignaturas_con_mayor_reprobacion", []):
        # ar es el dict de la metrica por asignatura
        tasa = ar.get("tasa_aprobacion")
        tasa_rep = round(100 - tasa, 2) if tasa is not None else "N/A"
        story.append(Paragraph(f"- {ar['asignatura_nombre']} — Tasa reprobación: {tasa_rep}%", styles['Normal']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Docentes con mejor promedio (Top)", styles['Heading2']))
    for d in resumen_global.get("docentes_con_mejor_promedio", []):
        story.append(Paragraph(f"- {d['docente_nombre']} — Promedio: {d['promedio']}", styles['Normal']))
    story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer
