from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        roles = {
            "Administrador": [
                "registrar_usuario",
                "enviar_codigo_recuperacion",
                "validar_codigo_recuperacion",
                "restablecer_password",
                "cambiar_password",
                "ver_roles",
                "asignar_roles",
                "crear_roles",
                "ver_permisos",
                "asignar_permisos",
                "crear_permisos",
                "view_user",
                "add_user",
                "change_user",
                "delete_user",
            ],
            "Coordinador": [
                "registrar_usuario",
                "view_user",
                "change_user",
            ],
            "Profesor": [],
            "Estudiante": [],
        }

        for role_name, permissions in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            for perm in permissions:
                try:
                    permission = Permission.objects.get(codename=perm)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"⚠ Permiso no encontrado: {perm}")

        self.stdout.write(self.style.SUCCESS("Roles creados exitosamente"))
