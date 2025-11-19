from django.urls import path
from asignaturas.views.asignaturas_view import (
    CrearAsignaturaView,
    ListarAsignaturasView,
    AsignaturaDetalleView
)

urlpatterns = [
    # Crear asignatura
    path("asignaturas/crear/", CrearAsignaturaView.as_view(), name="crear_asignatura"),

    # Listar asignaturas
    path("asignaturas/", ListarAsignaturasView.as_view(), name="lista_asignaturas"),

    # Obtener / Editar / Eliminar una asignatura
    path("asignaturas/<int:id>/", AsignaturaDetalleView.as_view(), name="detalle_asignatura"),
]
