from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

ROLES = (
    ('administrador', 'Administrador'),
    ('docente', 'Docente'),
    ('estudiante', 'Estudiante'),
    ('coordinador', 'Coordinador Académico'),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo es obligatorio")

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=email, **extra_fields)

        if not password:
            raise ValueError("El usuario debe tener contraseña")

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Meta:
        permissions = [
            ("usuarios_crear_usuario", "Puede crear usuarios"),
            ("usuarios_editar_usuario", "Puede editar usuarios"),
            ("roles_editar_rol", "Puede editar roles y permisos"),
        ]
        
    nombre = models.CharField(max_length=50, blank=True)
    apellido = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=30, choices=ROLES, blank=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # *** CORRECCIÓN CRÍTICA ***

    def __str__(self):
        return f"{self.email}"
    
    
