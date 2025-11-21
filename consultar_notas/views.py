from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from calificaciones.models import CalificacionEntrega
from .serializers import CalificacionEntregaSerializer

class ConsultaNotasEstudianteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        estudiante = request.user
        asignatura_id = request.GET.get('asignatura')
        periodo = request.GET.get('periodo')  # opcional si tu modelo soporta periodos

        # Filtramos calificaciones del estudiante
        qs = CalificacionEntrega.objects.filter(entrega__estudiante=estudiante)

        if asignatura_id:
            qs = qs.filter(entrega__tarea__asignatura_id=asignatura_id)

        # Filtro por periodo si aplica
        if periodo:
            qs = qs.filter(entrega__tarea__asignatura__periodo=periodo)

        serializer = CalificacionEntregaSerializer(qs, many=True)

        # Calculamos promedio ponderado
        promedio = 0
        for c in qs:
            peso = c.entrega.tarea.peso_porcentual
            promedio += float(c.nota) * (peso / 100)

        return Response({
            "tareas": serializer.data,
            "promedio_final": round(promedio, 2)
        })
