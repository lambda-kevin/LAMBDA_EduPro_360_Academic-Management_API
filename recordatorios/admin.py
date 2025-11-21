# recordatorios/admin.py

from django.contrib import admin
from .models import RecordatorioTarea

@admin.register(RecordatorioTarea)
class RecordatorioTareaAdmin(admin.ModelAdmin):
    list_display = ('tarea', 'estudiante', 'tipo_recordatorio', 'fecha_envio', 'enviado')
    list_filter = ('tipo_recordatorio', 'enviado')
    search_fields = ('tarea__titulo', 'estudiante__correo')
