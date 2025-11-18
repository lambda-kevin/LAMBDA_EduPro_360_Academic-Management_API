from django.contrib.auth.models import BaseUserManager


#-------------------------------------------------------------------------------
#creacion del usuario y validaciones 
class CustomUserManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El usuario debe tener un correo electrónico")

        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(correo, password, **extra_fields)
