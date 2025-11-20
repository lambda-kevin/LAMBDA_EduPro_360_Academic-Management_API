from rest_framework import serializers
from asignaturas.models import Asignatura

class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = "__all__"
            
    def validate_creditos(self, value):
        if value <= 0:
            raise serializers.ValidationError("Los créditos deben ser mayores a 0.")
        return value

    def validate_semestre(self, value):
        if value <= 0:
            raise serializers.ValidationError("El semestre debe ser mayor a 0.")
        return value
