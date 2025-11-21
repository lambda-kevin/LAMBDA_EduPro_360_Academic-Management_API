from django.urls import path
from .views import EjecutarRecordatoriosAPIView

urlpatterns = [
    path("recordatorios/enviar/", EjecutarRecordatoriosAPIView.as_view()),
]
