from rest_framework import serializers
from .models import RecordatorioTarea

class RecordatorioTareaSerializer(serializers.ModelSerializer):
    tarea_titulo = serializers.CharField(source='tarea.titulo', read_only=True)
    asignatura = serializers.CharField(source='tarea.asignatura.nombre', read_only=True)
    docente_responsable = serializers.CharField(source='tarea.asignatura.docente_responsable.email', read_only=True)
    estudiante_email = serializers.CharField(source='estudiante.email', read_only=True)

    class Meta:
        model = RecordatorioTarea
        fields = [
            'id',
            'tarea_titulo',
            'asignatura',
            'estudiante_email',
            'docente_responsable',
            'tipo_recordatorio',
            'fecha_envio',
            'enviado',
        ]
