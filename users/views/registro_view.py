from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import RegistroUsuarioSerializer
from ..services import enviar_correo_bienvenida



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
    