from django.db import models
from entrega_tareas.models import EntregaTarea
from users.models import CustomUser
from asignaturas.models import Asignatura


class CalificacionEntrega(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('publicado', 'Publicado'),
    )

    entrega = models.OneToOneField(EntregaTarea, on_delete=models.CASCADE, related_name='calificacion')
    docente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='calificaciones_realizadas')
    nota = models.DecimalField(max_digits=3, decimal_places=1)  # ejemplo 4.5
    retroalimentacion_docente = models.TextField(blank=True)
    fecha_calificacion = models.DateTimeField(auto_now_add=True)
    estado_calificacion = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    class Meta:
        permissions = [
            ("calificar_tareas", "Puede calificar tareas"),
            ("ver_calificaciones", "Puede ver calificaciones"),
        ]

    def __str__(self):
        return f"Calificación de {self.entrega.estudiante} para {self.entrega.tarea}"


# ==========================================================
# NOTA FINAL POR ASIGNATURA
# ==========================================================
class NotaFinalAsignatura(models.Model):
    estudiante = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notas_finales')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='notas_finales')
    nota_final = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        unique_together = ("estudiante", "asignatura")

    def __str__(self):
        return f"{self.estudiante} - {self.asignatura} : {self.nota_final}"
