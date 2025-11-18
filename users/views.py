from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistroUsuarioSerializer
from .services import enviar_correo_bienvenida
from .serializers import LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings

from .serializers import CambioContraseñaSerializer

#______________________________________________________________________
#registro de usuarios con sus roles
class RegistroUsuarioView(APIView):

    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)

        if serializer.is_valid():
            usuario = serializer.save()

            # Enviar correo de bienvenida
            enviar_correo_bienvenida(usuario.correo, usuario.nombre)

            return Response(
                {"mensaje": "Usuario registrado correctamente"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#--------------------------------------------------------------------------------
#inicio de sesion 

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Inicio de sesión:
        - Validar correo + contraseña
        - Generar access + refresh tokens (Simple JWT)
        - Actualizar last_login
        - Devolver datos del usuario y tokens
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        usuario = serializer.validated_data["usuario"]

        # Generar tokens JWT
        refresh = RefreshToken.for_user(usuario)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Actualizar last_login (solo ese campo para no tocar otros campos)
        try:
            usuario.last_login = timezone.now()
            usuario.save(update_fields=["last_login"])
        except Exception:
            # No queremos que un fallo al guardar last_login afecte el login
            pass

        respuesta = {
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {
                "id": getattr(usuario, "id", None),
                "nombre": getattr(usuario, "nombre", ""),
                "apellido": getattr(usuario, "apellido", ""),
                "correo": getattr(usuario, "correo", ""),
                "rol": getattr(usuario, "rol", ""),
            },
            "tokens": {
                "access": access_token,
                "refresh": refresh_token
            }
        }

        return Response(respuesta, status=status.HTTP_200_OK)
#-----------------------------------------------------------------------
#cambio de contraseña


class CambioContraseñaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CambioContraseñaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contraseña_actual = serializer.validated_data["contraseña_actual"]
        nueva_contraseña = serializer.validated_data["nueva_contraseña"]

        usuario = request.user

        # Validar contraseña actual
        if not usuario.check_password(contraseña_actual):
            return Response(
                {"error": "La contraseña actual es incorrecta."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Guardar nueva contraseña
        usuario.set_password(nueva_contraseña)
        usuario.save()

     # Enviar correo de confirmación
        send_mail(
            subject="Cambio de contraseña exitoso",
            message="Tu contraseña ha sido actualizada correctamente.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.correo],
            fail_silently=False,
        )

        return Response({"mensaje": "Contraseña actualizada correctamente."}, status=200)
#--------------------------------------------------------------------------------------------
#recuperacion de contraseña


