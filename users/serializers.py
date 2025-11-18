from rest_framework import serializers
from .models import CustomUser
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password

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
