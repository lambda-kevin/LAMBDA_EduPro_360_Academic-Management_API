from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone


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