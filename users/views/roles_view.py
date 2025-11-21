from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import TienePermiso
from users.models import Rol, Permiso, UsuarioRol, CustomUser

from users.serializers import (
    RolSerializer,
    PermisoSerializer,
    AsignarRolSerializer
)


# ================================
#        PERMISOS
# ================================
class CrearPermisoView(APIView):
    permission_classes = [IsAuthenticated, TienePermiso]
    permiso_requerido = "crear_permisos"  # nombre del permiso que debe tener el rol

    def post(self, request):
        serializer = PermisoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Permiso creado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ListaPermisosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        permisos = Permiso.objects.all()
        serializer = PermisoSerializer(permisos, many=True)
        return Response(serializer.data, status=200)


# ================================
#        ROLES
# ================================
class CrearRolView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class ListaRolesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data, status=200)


# ================================
#   ASIGNAR PERMISOS A ROLES
# ================================
class AsignarPermisoRolView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        rol_id = request.data.get("rol_id")
        permiso_id = request.data.get("permiso_id")

        if not rol_id or not permiso_id:
            return Response({"error": "rol_id y permiso_id son requeridos"}, status=400)

        try:
            rol = Rol.objects.get(id=rol_id)
            permiso = Permiso.objects.get(id=permiso_id)
        except Rol.DoesNotExist:
            return Response({"error": "El rol no existe"}, status=404)
        except Permiso.DoesNotExist:
            return Response({"error": "El permiso no existe"}, status=404)

        rol.permisos.add(permiso)
        return Response({"mensaje": "Permiso asignado al rol correctamente"}, status=200)


# ================================
#      ASIGNAR ROLES A USUARIOS
# ================================
class AsignarRolUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AsignarRolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario_id = serializer.validated_data["usuario_id"]
        rol_id = serializer.validated_data["rol_id"]

        try:
            usuario = CustomUser.objects.get(id=usuario_id)
            rol = Rol.objects.get(id=rol_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "El usuario no existe"}, status=404)
        except Rol.DoesNotExist:
            return Response({"error": "El rol no existe"}, status=404)

        UsuarioRol.objects.create(usuario=usuario, rol=rol)
        return Response({"mensaje": "Rol asignado correctamente"}, status=200)


# ================================
#   LISTAR ROLES DE UN USUARIO
# ================================
class RolesDeUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, usuario_id):
        if not CustomUser.objects.filter(id=usuario_id).exists():
            return Response({"error": "Usuario no encontrado"}, status=404)

        roles = UsuarioRol.objects.filter(usuario_id=usuario_id).select_related("rol")
        data = [{"rol_id": r.rol.id, "nombre": r.rol.nombre} for r in roles]

        return Response(data, status=200)


# ================================
#   REMOVER ROL A UN USUARIO
# ================================
class RemoverRolUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        usuario_id = request.data.get("usuario_id")
        rol_id = request.data.get("rol_id")

        if not usuario_id or not rol_id:
            return Response({"error": "usuario_id y rol_id son requeridos"}, status=400)

        deleted = UsuarioRol.objects.filter(usuario_id=usuario_id, rol_id=rol_id).delete()

        if deleted[0] == 0:
            return Response({"error": "El rol no estaba asignado"}, status=404)

        return Response({"mensaje": "Rol removido correctamente"}, status=200)
