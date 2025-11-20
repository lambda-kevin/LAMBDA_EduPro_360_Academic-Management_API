from django.db.models.signals import post_migrate
from django.dispatch import receiver
from users.models import Permiso

@receiver(post_migrate)
def crear_permisos_asignaturas(sender, **kwargs):
    """
    Crea automáticamente los permisos de la app Asignaturas
    después de ejecutar las migraciones.
    """
    if sender.label != "asignaturas":
        return

    permisos = [
        ("ver_asignaturas", "Puede ver asignaturas"),
        ("crear_asignatura", "Puede crear asignaturas"),
        ("editar_asignatura", "Puede editar asignaturas"),
        ("eliminar_asignatura", "Puede eliminar asignaturas"),
    ]

    for nombre, descripcion in permisos:
        Permiso.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})
