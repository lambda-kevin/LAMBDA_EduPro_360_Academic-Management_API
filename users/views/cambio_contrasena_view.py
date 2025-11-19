from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings

from users.serializers import CambioContraseñaSerializer


#---------------------------------------------------------------------------
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