from django.urls import path
from .views import RegistroUsuarioView

urlpatterns = [
    path("registrar/", RegistroUsuarioView.as_view(), name="registrar_usuario"),
    
]
