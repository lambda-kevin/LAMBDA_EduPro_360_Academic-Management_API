from django.urls import path
from .views import CalificarEntregaView

urlpatterns = [
    path("calificar/<int:entrega_id>/", CalificarEntregaView.as_view(), name="calificar_entrega"),
]
