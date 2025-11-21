# recordatorios/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .tasks import generar_reporte_mensual

from users.permissions import TienePermiso

class ForzarGeneracionReporteAPIView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso]
    permiso_requerido = "recibir_notificacion_estado_mensual"  # o un permiso administrativo si prefieres

    def post(self, request):
        """
        Opcional: acepta body con 'anio' y 'mes' para forzar un mes concreto.
        Si no se pasan, generará para el mes anterior.
        """
        anio = request.data.get("anio")
        mes = request.data.get("mes")

        # lanzar tarea asincrónica
        if anio and mes:
            generar_reporte_mensual.delay(int(anio), int(mes))
        else:
            generar_reporte_mensual.delay()

        return Response({"mensaje": "Generación del reporte encolada"}, status=status.HTTP_202_ACCEPTED)
