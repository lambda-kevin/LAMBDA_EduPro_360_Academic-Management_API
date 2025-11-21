from django.urls import path
from .views import ConsultaNotasEstudianteView

urlpatterns = [
    path(
        "estudiante/notas/",
        ConsultaNotasEstudianteView.as_view(),
        name="consulta_notas_estudiante"
    ),
]
