from rest_framework import viewsets, permissions
from tareas.models import Tarea
from tareas.serializers.tarea_serializer import TareaSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtrar solo tareas activas si es necesario
        return Tarea.objects.filter(estado='activo')
