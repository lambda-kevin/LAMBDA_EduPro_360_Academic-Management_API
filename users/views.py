from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import UserUpdateSerializer, RoleSerializer, PermissionSerializer, UserRoleAssignSerializer
from django.contrib.auth.models import Group, Permission

# ---------------------------------------------
# LOGIN
# ---------------------------------------------
class LoginView(APIView):
    """
    Login por email usando JWT.
    IMPORTANTE: Django authenticate usa 'username' internamente,
    aunque nuestro USERNAME_FIELD = 'email'.
    """

    def get(self, request):
        return Response(
            {"detail": "Use POST para iniciar sesión."},
            status=status.HTTP_200_OK
        )
    
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email y contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        # Autenticación
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'Usuario inactivo'}, status=status.HTTP_403_FORBIDDEN)

        # Crear tokens JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'rol': user.rol,
            'nombre': user.nombre,
            'apellido': user.apellido,
        })

# ---------------------------------------------
# ACTUALIZAR USUARIO (solo admins)
# ---------------------------------------------
class UserUpdateView(RetrieveUpdateAPIView):
    """
    Permite a un administrador actualizar datos de un usuario.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

# ---------------------------------------------
# VISTAS PARA ROLES Y PERMISOS
# ---------------------------------------------
class RoleViewSet(viewsets.ModelViewSet):
    """
    Endpoints CRUD para los roles (grupos).
    Solo accesible por superusuario o admin.
    """
    queryset = Group.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]

class PermissionListView(APIView):
    """
    Endpoint para listar todos los permisos del sistema.
    Útil para asignarlos a roles.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        permisos = Permission.objects.all()
        serializer = PermissionSerializer(permisos, many=True)
        return Response(serializer.data)

class UserRoleAssignView(APIView):
    """
    Endpoint para asignar roles (grupos) a un usuario.
    Solo accesible por admin.
    """
    permission_classes = [IsAdminUser]
   
    def get(self, request, pk):
        return Response(
            {"detail": "Use POST para asignar roles a este usuario."},
            status=status.HTTP_200_OK
        )


    def post(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRoleAssignSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Roles asignados correctamente"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
