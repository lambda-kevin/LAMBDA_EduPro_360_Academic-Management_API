from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from calificaciones.serializers import CalificarEntregaSerializer
from calificaciones.models import CalificacionEntrega
from entrega_tareas.models import EntregaTarea
from users.permissions import TienePermiso


class CalificarEntregaView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso]
    permiso_requerido = "calificar_entregas"

    def post(self, request, entrega_id):

        # Verificar que la entrega exista
        try:
            entrega = EntregaTarea.objects.get(id=entrega_id)
        except EntregaTarea.DoesNotExist:
            return Response({"error": "Entrega no encontrada"}, status=404)

        # Verificar si ya existe calificación
        if hasattr(entrega, 'calificacion'):
            calificacion = entrega.calificacion
            serializer = CalificarEntregaSerializer(calificacion, data=request.data, partial=True)
        else:
            serializer = CalificarEntregaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(docente=request.user, entrega=entrega)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
