from django.db import models

class Asignatura(models.Model):
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True)
    creditos = models.IntegerField()
    semestre = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
