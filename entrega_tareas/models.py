from django.db import models
from tareas.models import Tarea
from users.models import CustomUser

class EntregaTarea(models.Model):
	ESTADO_CHOICES = (
		('entregado', 'Entregado'),
		('revisado', 'Revisado'),
		('atrasado', 'Atrasado'),
	)
	tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='entregas')
	estudiante = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='entregas')
	archivo_entrega = models.FileField(upload_to='entregas/')
	comentarios_estudiante = models.TextField(blank=True)
	fecha_entrega = models.DateTimeField(auto_now_add=True)
	estado_entrega = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='entregado')

	def __str__(self):
		return f"Entrega de {self.estudiante} para {self.tarea}"
