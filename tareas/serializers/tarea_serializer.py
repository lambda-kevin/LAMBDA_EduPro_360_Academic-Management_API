from rest_framework import serializers
from tareas.models import Tarea

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

    def validate(self, data):
        # Validación de fechas
        if data['fecha_vencimiento'] < data['fecha_publicacion']:
            raise serializers.ValidationError("La fecha de vencimiento no puede ser anterior a la fecha de publicación.")
        # Validación de suma de pesos
        asignatura = data['asignatura']
        peso_nuevo = data['peso_porcentual']
        tareas = Tarea.objects.filter(asignatura=asignatura)
        if self.instance:
            tareas = tareas.exclude(pk=self.instance.pk)
        suma_pesos = sum(t.peso_porcentual for t in tareas) + peso_nuevo
        if suma_pesos > 100:
            raise serializers.ValidationError("La suma de los pesos porcentuales supera el 100%.")
        return data
