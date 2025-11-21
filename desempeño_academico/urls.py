# recordatorios/urls.py

from django.urls import path
from .views import ForzarGeneracionReporteAPIView

urlpatterns = [
    path("reporte/mensual/forzar/", ForzarGeneracionReporteAPIView.as_view(), name="forzar_reporte_mensual"),
]
