from rest_framework import serializers
from entrega_tareas.models import EntregaTarea
from tareas.models import Tarea
from django.utils import timezone

class EntregaTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntregaTarea
        fields = '__all__'

    def validate(self, data):
        tarea = data['tarea']
        fecha_vencimiento = tarea.fecha_vencimiento
        fecha_entrega = timezone.now()
        if fecha_entrega > fecha_vencimiento:
            raise serializers.ValidationError("La entrega se realizó fuera del plazo permitido.")
        return data
