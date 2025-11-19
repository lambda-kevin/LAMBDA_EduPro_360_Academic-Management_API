from rest_framework import serializers
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from users.models import CustomUser, Rol, Permiso, UsuarioRol
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
import re


Usuario = get_user_model()

# =====================================================================================
# REGISTRO DE USUARIO
# =====================================================================================

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[
            validate_password,
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$',
                message="La contraseña debe tener al menos una mayúscula, un número y un carácter especial."
            )
        ]
    )

    class Meta:
        model = CustomUser
        fields = ["nombre", "apellido", "correo", "password", "rol", "estado"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        rol = validated_data.get("rol")

        # Crear usuario
        usuario = CustomUser.objects.create_user(password=password, **validated_data)

        # ⬅ Rol automático en tabla intermedia
        if rol:
            UsuarioRol.objects.create(usuario=usuario, rol=rol)

        return usuario


# =====================================================================================
# LOGIN
# =====================================================================================

class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    nombre = serializers.CharField(read_only=True)
    apellido = serializers.CharField(read_only=True)
    rol = serializers.CharField(read_only=True)

    def validate(self, data):
        correo = data.get("correo")
        password = data.get("password")

        try:
            usuario = Usuario.objects.get(correo__iexact=correo)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"detalle": "Credenciales inválidas."})

        if not usuario.is_active:
            raise serializers.ValidationError({"detalle": "Usuario inactivo."})

        if hasattr(usuario, "estado") and usuario.estado is False:
            raise serializers.ValidationError({"detalle": "Usuario deshabilitado."})

        if not usuario.check_password(password):
            raise serializers.ValidationError({"detalle": "Credenciales inválidas."})

        data["usuario"] = usuario
        return data


# =====================================================================================
# CAMBIO DE CONTRASEÑA
# =====================================================================================

class CambioContraseñaSerializer(serializers.Serializer):
    contraseña_actual = serializers.CharField(required=True)
    nueva_contraseña = serializers.CharField(required=True)

    def validar_nueva_contraseña(self, value):
        patron = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&._-]).{8,}$'
        if not re.match(patron, value):
            raise serializers.ValidationError(
                "La contraseña debe tener al menos una mayúscula, un número y un carácter especial."
            )
        return value


# =====================================================================================
# RECUPERACIÓN DE CONTRASEÑA
# =====================================================================================

class SolicitarRecuperacionSerializer(serializers.Serializer):
    correo = serializers.EmailField()


class ValidarTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class RestablecerContraseñaSerializer(serializers.Serializer):
    token = serializers.CharField()
    nueva_contraseña = serializers.CharField(write_only=True)


# =====================================================================================
# SISTEMA DE ROLES Y PERMISOS (HU-5)
# =====================================================================================

class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = "__all__"


class RolSerializer(serializers.ModelSerializer):
    permisos = PermisoSerializer(many=True, read_only=True)
    permisos_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Rol
        fields = ["id", "nombre", "descripcion", "permisos", "permisos_ids"]

    def create(self, validated_data):
        permisos_ids = validated_data.pop("permisos_ids", [])
        rol = Rol.objects.create(**validated_data)
        rol.permisos.set(permisos_ids)
        return rol

    def update(self, instance, validated_data):
        permisos_ids = validated_data.pop("permisos_ids", None)
        instance = super().update(instance, validated_data)

        if permisos_ids is not None:
            instance.permisos.set(permisos_ids)

        return instance


class AsignarRolSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    rol_id = serializers.IntegerField()

    def validate(self, data):
        try:
            data["usuario"] = CustomUser.objects.get(id=data["usuario_id"])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("El usuario no existe.")

        try:
            data["rol"] = Rol.objects.get(id=data["rol_id"])
        except Rol.DoesNotExist:
            raise serializers.ValidationError("El rol no existe.")

        return data

    def create(self, validated_data):
        usuario = validated_data["usuario"]
        rol = validated_data["rol"]

        UsuarioRol.objects.update_or_create(
            usuario=usuario,
            defaults={"rol": rol}
        )
        return validated_data
