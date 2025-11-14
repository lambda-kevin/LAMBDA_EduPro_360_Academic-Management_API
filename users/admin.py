from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from .models import CustomUser

# Desregistramos el grupo para personalizar su visualización
admin.site.unregister(Group)

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin personalizado para CustomUser.
    Permite:
    - Gestión completa de usuarios
    - Asignación de roles/grupos y permisos específicos
    """
    model = CustomUser

    # Qué se muestra en la lista de usuarios
    list_display = ('email', 'nombre', 'apellido', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active', 'groups')

    # Campos al editar un usuario
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('nombre', 'apellido', 'rol', 'estado')}),
        ('Permisos', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',          # Permite asignar roles/grupos
                'user_permissions' # Permite asignar permisos individuales
            ),
        }),
        ('Fechas', {'fields': ('fecha_creacion',)}),
    )

    # Campos al crear un usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'nombre', 'apellido', 'rol',
                'password1', 'password2',
                'is_active', 'is_staff'
            ),
        }),
    )

    search_fields = ('email', 'nombre', 'apellido')
    ordering = ('email',)

# Admin para manejar Grupos/roles
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Admin para gestionar Grupos/roles.
    Permite:
    - Ver permisos asignados a cada grupo
    - Asignar permisos desde el admin
    """
    list_display = ('name',)
    filter_horizontal = ('permissions',)  # Mejor interfaz para asignar permisos
    search_fields = ('name',)

# Admin opcional para ver Permisos directamente
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """
    Admin para ver permisos del sistema.
    Normalmente no se modifican directamente, pero útil para depuración.
    """
    list_display = ('name', 'codename', 'content_type')
    search_fields = ('name', 'codename')
