from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.conf import settings

#creacion de tabla con sus colomnas 
class CustomUser(AbstractBaseUser, PermissionsMixin):

    #__________________________________________________________________
    #permisos de roles
    class Meta:
        permissions = [
            ("registrar_usuario", "Puede registrar usuarios"),
            ("enviar_codigo_recuperacion", "Puede enviar códigos de recuperación"),
            ("validar_codigo_recuperacion", "Puede validar códigos de recuperación"),
            ("restablecer_password", "Puede restablecer contraseñas"),
            ("cambiar_password", "Puede cambiar la contraseña"),

            ("ver_roles", "Puede ver roles del sistema"),
            ("asignar_roles", "Puede asignar roles"),
            ("crear_roles", "Puede crear nuevos roles"),

            ("ver_permisos", "Puede ver permisos"),
            ("asignar_permisos", "Puede asignar permisos"),
            ("crear_permisos", "Puede crear nuevos permisos"),
        ]
    #__________________________________________________________________
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    # Datos administrativos requeridos por Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    rol = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["nombre", "apellido"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

#-----------------------------------------------------------------------

class Permiso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    permisos = models.ManyToManyField(Permiso, related_name="roles", blank=True)

    def __str__(self):
        return self.nombre


class UsuarioRol(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="roles_asignados")
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name="usuarios")

    class Meta:
        unique_together = ("usuario", "rol")

    def __str__(self):
        return f"{self.usuario.correo} - {self.rol.nombre}"
