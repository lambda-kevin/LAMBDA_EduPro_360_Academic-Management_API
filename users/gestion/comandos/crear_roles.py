from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Crea los roles base y asigna permisos según el HU map'

    def handle(self, *args, **options):
        # Diccionario de roles → lista de permisos (app_label.codename)
        permisos_por_rol = {
            "Administrador": [
                "users.crear_usuario",
                "users.editar_usuario",
                "users.editar_rol",
                "academico.ver_asignatura",
                "tareas.ver_tarea",
            ],
            "Coordinador": [
                "academico.crear_asignatura",
                "academico.asignar_docente",
                "notificaciones.generar_reporte_mensual",
                "notificaciones.recibir_notificacion_estado_mensual",
            ],
            "Docente": [
                "tareas.crear_tarea",
                "tareas.editar_tarea",
                "entregas.ver_entrega",
                "calificaciones.calificar_tarea",
            ],
            "Estudiante": [
                "entregas.subir_entrega",
                "estudiantes.ver_calificaciones_propias",
            ],
        }

        for nombre_rol, permisos in permisos_por_rol.items():
            grupo, creado = Group.objects.get_or_create(name=nombre_rol)
            if creado:
                self.stdout.write(self.style.SUCCESS(f"Grupo creado: {nombre_rol}"))
            else:
                self.stdout.write(f"Grupo existente: {nombre_rol}")

            # Limpiar permisos actuales para reemplazarlos
            grupo.permissions.clear()

            for perm in permisos:
                try:
                    app_label, codename = perm.split(".")
                except ValueError:
                    self.stdout.write(self.style.ERROR(f"Permiso inválido '{perm}'"))
                    continue

                permission = Permission.objects.filter(
                    content_type__app_label=app_label,
                    codename=codename
                ).first()

                if permission:
                    grupo.permissions.add(permission)
                    self.stdout.write(f"  → Asignado {perm} a {nombre_rol}")
                else:
                    self.stdout.write(self.style.WARNING(f"  ! Permiso no encontrado: {perm}"))

            grupo.save()

        self.stdout.write(self.style.SUCCESS("¡Proceso de creación de roles finalizado!"))
