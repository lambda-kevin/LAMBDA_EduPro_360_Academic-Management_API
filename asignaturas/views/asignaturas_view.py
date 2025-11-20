from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from asignaturas.models import Asignatura
from asignaturas.serializers.asignaturas_serializer import AsignaturaSerializer
from users.permissions import TienePermiso


# ============================================================
# CREAR ASIGNATURA
# ============================================================
class CrearAsignaturaView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso]
    permiso_requerido = "crear_asignatura"

    def post(self, request):
        serializer = AsignaturaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ============================================================
# LISTAR ASIGNATURAS
# ============================================================
class ListarAsignaturasView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso]
    permiso_requerido = "ver_asignaturas"

    def get(self, request):
        asignaturas = Asignatura.objects.all()
        serializer = AsignaturaSerializer(asignaturas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================================
# DETALLE / EDITAR / ELIMINAR ASIGNATURA
# ============================================================
class AsignaturaDetalleView(APIView):

    # ----------------------- GET ------------------------------
    permiso_requerido = None  # se define dinámicamente

    def get(self, request, id):
        self.permiso_requerido = "ver_asignaturas"
        self.permission_classes = [IsAuthenticated, TienePermiso]
        self.check_permissions(request)

        try:
            asignatura = Asignatura.objects.get(id=id)
        except Asignatura.DoesNotExist:
            return Response({"error": "Asignatura no encontrada"}, status=404)

        serializer = AsignaturaSerializer(asignatura)
        return Response(serializer.data, status=200)

    # ----------------------- PUT ------------------------------
    def put(self, request, id):
        self.permiso_requerido = "editar_asignatura"
        self.permission_classes = [IsAuthenticated, TienePermiso]
        self.check_permissions(request)

        try:
            asignatura = Asignatura.objects.get(id=id)
        except Asignatura.DoesNotExist:
            return Response({"error": "Asignatura no encontrada"}, status=404)

        serializer = AsignaturaSerializer(asignatura, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

    # ----------------------- DELETE ------------------------------
    def delete(self, request, id):
        self.permiso_requerido = "eliminar_asignatura"
        self.permission_classes = [IsAuthenticated, TienePermiso]
        self.check_permissions(request)

        try:
            asignatura = Asignatura.objects.get(id=id)
        except Asignatura.DoesNotExist:
            return Response({"error": "Asignatura no encontrada"}, status=404)

        asignatura.delete()
        return Response({"mensaje": "Asignatura eliminada correctamente"}, status=200)
