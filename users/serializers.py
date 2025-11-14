from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from .models import CustomUser

# ---------------------------------------------
# SERIALIZER PARA ACTUALIZAR USUARIOS
# ---------------------------------------------
class UserUpdateSerializer(serializers.ModelSerializer):
    # Manejo correcto del campo ManyToMany "groups"
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'nombre',
            'apellido',
            'email',
            'rol',        # Campo visual de referencia
            'estado',
            'is_active',
            'is_staff',
            'groups'
        ]
        extra_kwargs = {
            'email': {'read_only': True},  # No se permite cambiar el email
        }

    def update(self, instance, validated_data):
        """
        Sobrescribir update para manejar correctamente la relación ManyToMany 'groups'.
        """
        groups = validated_data.pop('groups', None)

        # Actualizar campos normales
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Actualizar grupos si vienen en la petición
        if groups is not None:
            instance.groups.set(groups)

        return instance

# ---------------------------------------------
# SERIALIZER PARA PERMISOS
# ---------------------------------------------
class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar permisos existentes en el sistema.
    """
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']

# ---------------------------------------------
# SERIALIZER PARA ROLES (GRUPOS)
# ---------------------------------------------
class RoleSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar y editar roles (grupos).
    Incluye los permisos asociados.
    """
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions', None)

        # Actualizar nombre del grupo si viene
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Actualizar permisos si vienen
        if permissions is not None:
            instance.permissions.set(permissions)

        return instance

# ---------------------------------------------
# SERIALIZER PARA ASIGNAR ROLES A USUARIOS
# ---------------------------------------------
class UserRoleAssignSerializer(serializers.ModelSerializer):
    """
    Serializador para asignar roles (grupos) a un usuario.
    """
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'groups']

    def update(self, instance, validated_data):
        groups = validated_data.get('groups', None)
        if groups is not None:
            instance.groups.set(groups)
        instance.save()
        return instance
