from django.db import models
from users.models import CustomUser

class Asignatura(models.Model):
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True)
    creditos = models.IntegerField()
    semestre = models.IntegerField()
    docente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='asignaturas', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
