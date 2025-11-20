from rest_framework import serializers
from calificaciones.models import CalificacionEntrega
from tareas.models import Tarea

class CalificacionEntregaSerializer(serializers.ModelSerializer):
    titulo_tarea = serializers.CharField(source='entrega.tarea.titulo')
    tipo_tarea = serializers.CharField(source='entrega.tarea.tipo_tarea')
    peso_porcentual = serializers.IntegerField(source='entrega.tarea.peso_porcentual')

    class Meta:
        model = CalificacionEntrega
        fields = [
            'titulo_tarea',
            'tipo_tarea',
            'nota',
            'peso_porcentual',
            'retroalimentacion_docente',
            'estado_calificacion',
            'fecha_calificacion'
        ]
