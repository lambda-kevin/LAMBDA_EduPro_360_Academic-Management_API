from rest_framework import serializers
from .models import CalificacionEntrega

class CalificarEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalificacionEntrega
        fields = [
            "id",
            "entrega",
            "docente",
            "nota",
            "retroalimentacion_docente",
            "fecha_calificacion",
            "estado_calificacion"
        ]
        read_only_fields = ["fecha_calificacion", "docente"]
