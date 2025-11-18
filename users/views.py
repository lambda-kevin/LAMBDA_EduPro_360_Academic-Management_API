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
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

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


from .serializers import (
    SolicitarRecuperacionSerializer,
    ValidarTokenSerializer,
    RestablecerContraseñaSerializer
)

Usuario = get_user_model()
signer = TimestampSigner()


# -------------------------------
# 1. Solicitar recuperación
# -------------------------------
class SolicitarRecuperacionView(APIView):
    def post(self, request):
        serializer = SolicitarRecuperacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        correo = serializer.validated_data["correo"]

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            usuario = None

        # Seguridad: NO revelar si el usuario existe o no
        if usuario:
            token = signer.sign(correo)

            enlace = f"http://localhost:5173/restablecer?token={token}"

            send_mail(
                subject="Recuperación de contraseña",
                message=f"Para restablecer tu contraseña usa este enlace:\n\n{enlace}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[correo]
            )

        return Response({"mensaje": "Si el correo existe, enviaremos instrucciones."})


# -------------------------------
# 2. Validar token
# -------------------------------
class ValidarTokenView(APIView):
    def post(self, request):
        serializer = ValidarTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]

        try:
            correo = signer.unsign(token, max_age=3600)  # 1 hora
            return Response({"valido": True, "correo": correo})
        except SignatureExpired:
            return Response({"error": "El enlace ha expirado."}, status=400)
        except BadSignature:
            return Response({"error": "Token inválido."}, status=400)


# -------------------------------
# 3. Restablecer contraseña
# -------------------------------
class RestablecerContraseñaView(APIView):
    def post(self, request):
        serializer = RestablecerContraseñaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        nueva = serializer.validated_data["nueva_contraseña"]

        try:
            correo = signer.unsign(token, max_age=3600)
        except SignatureExpired:
            return Response({"error": "El enlace ha expirado."}, status=400)
        except BadSignature:
            return Response({"error": "Token inválido."}, status=400)

        usuario = Usuario.objects.get(correo=correo)

        usuario.set_password(nueva)
        usuario.save()

        send_mail(
            subject="Contraseña actualizada",
            message="Tu contraseña fue restablecida correctamente.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[correo]
        )

        return Response({"mensaje": "Contraseña restablecida correctamente."})

