from rest_framework import serializers
from .models import CustomUser
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[
            validate_password,
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$',
                message="La contraseña debe tener al menos una mayúscula, un número, un caracter especial y mínimo 8 caracteres."
            )
        ]
    )

    class Meta:
        model = CustomUser
        fields = ["nombre", "apellido", "correo", "password", "rol", "estado"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        usuario = CustomUser.objects.create_user(password=password, **validated_data)
        return usuario
#---------------------------------------------------------------------------------------------
# inicio de sesion: 


Usuario = get_user_model()

class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    # Campos de salida (opcional)
    nombre = serializers.CharField(read_only=True)
    apellido = serializers.CharField(read_only=True)
    rol = serializers.CharField(read_only=True)

    def validate(self, data):
        correo = data.get("correo")
        password = data.get("password")

        # Buscar usuario por correo
        try:
            usuario = Usuario.objects.get(correo__iexact=correo)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"detalle": "Credenciales inválidas."})

        # Validar estado activo y campo 'estado' (si lo usas)
        if not getattr(usuario, "is_active", True):
            raise serializers.ValidationError({"detalle": "Usuario inactivo."})

        if hasattr(usuario, "estado") and usuario.estado is False:
            raise serializers.ValidationError({"detalle": "Usuario deshabilitado."})

        # Validar contraseña
        if not usuario.check_password(password):
            raise serializers.ValidationError({"detalle": "Credenciales inválidas."})

        # OK: inyectar usuario validado
        data["usuario"] = usuario
        return data
