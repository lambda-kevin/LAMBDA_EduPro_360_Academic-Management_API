from django.core.management.base import BaseCommand
from users.models import Permiso, Rol

class Command(BaseCommand):
    help = "Crea el permiso recibir_notificacion_estado_mensual y lo asigna a roles indicados"

    def handle(self, *args, **options):
        perm, created = Permiso.objects.get_or_create(
            nombre="recibir_notificacion_estado_mensual",
            defaults={"descripcion": "Recibe reporte mensual consolidado por correo"}
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Permiso creado"))
        else:
            self.stdout.write(self.style.WARNING("Permiso ya existía"))

        # Asignar a roles comunes
        roles_a_asignar = ["administrador", "coordinador"]
        for rn in roles_a_asignar:
            try:
                rol = Rol.objects.get(nombre__iexact=rn)
                rol.permisos.add(perm)
                self.stdout.write(self.style.SUCCESS(f"Permiso asignado a rol {rn}"))
            except Rol.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Rol {rn} no existe"))
