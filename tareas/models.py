
from django.db import models
from asignaturas.models import Asignatura

class Tarea(models.Model):
	TIPO_CHOICES = (
		('tarea', 'Tarea'),
		('examen', 'Examen'),
	)
	ESTADO_CHOICES = (
		('activo', 'Activo'),
		('inactivo', 'Inactivo'),
	)
	asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='tareas')
	titulo = models.CharField(max_length=255)
	descripcion = models.TextField()
	fecha_publicacion = models.DateField()
	fecha_vencimiento = models.DateField()
	peso_porcentual = models.PositiveIntegerField()
	tipo_tarea = models.CharField(max_length=10, choices=TIPO_CHOICES)
	estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')

	def __str__(self):
		return f"{self.titulo} ({self.tipo_tarea})"
