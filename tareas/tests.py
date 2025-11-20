
from django.test import TestCase
from tareas.models import Tarea
from asignaturas.models import Asignatura
from django.contrib.auth import get_user_model
from datetime import date, timedelta

class TareaModelTest(TestCase):
	def setUp(self):
		self.asignatura = Asignatura.objects.create(nombre='Matemáticas')

	def test_fecha_vencimiento_invalida(self):
		tarea = Tarea(
			asignatura=self.asignatura,
			titulo='Tarea 1',
			descripcion='Desc',
			fecha_publicacion=date.today(),
			fecha_vencimiento=date.today() - timedelta(days=1),
			peso_porcentual=50,
			tipo_tarea='tarea',
			estado='activo'
		)
		with self.assertRaises(Exception):
			tarea.full_clean()

	def test_suma_pesos_supera_100(self):
		Tarea.objects.create(
			asignatura=self.asignatura,
			titulo='Tarea 1',
			descripcion='Desc',
			fecha_publicacion=date.today(),
			fecha_vencimiento=date.today() + timedelta(days=5),
			peso_porcentual=60,
			tipo_tarea='tarea',
			estado='activo'
		)
		tarea2 = Tarea(
			asignatura=self.asignatura,
			titulo='Tarea 2',
			descripcion='Desc',
			fecha_publicacion=date.today(),
			fecha_vencimiento=date.today() + timedelta(days=10),
			peso_porcentual=50,
			tipo_tarea='tarea',
			estado='activo'
		)
		# Simular validación en el serializer
		from tareas.serializers.tarea_serializer import TareaSerializer
		serializer = TareaSerializer(data={
			'asignatura': self.asignatura.id,
			'titulo': tarea2.titulo,
			'descripcion': tarea2.descripcion,
			'fecha_publicacion': tarea2.fecha_publicacion,
			'fecha_vencimiento': tarea2.fecha_vencimiento,
			'peso_porcentual': tarea2.peso_porcentual,
			'tipo_tarea': tarea2.tipo_tarea,
			'estado': tarea2.estado
		})
		self.assertFalse(serializer.is_valid())
		self.assertIn('La suma de los pesos porcentuales supera el 100%.', str(serializer.errors))
