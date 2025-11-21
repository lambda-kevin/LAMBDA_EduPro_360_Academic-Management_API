from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import TienePermiso
from recordatorios.tasks import enviar_recordatorios_tareas

class EjecutarRecordatoriosAPIView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso]
    permiso_requerido = "enviar_recordatorios"

    def post(self, request):
        enviar_recordatorios_tareas.delay()
        return Response({"message": "Recordatorios en cola para envíos"}, status=200)
