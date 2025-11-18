from django.urls import path
from .views import RegistroUsuarioView
from .views import LoginView
from .views import CambioContraseñaView

urlpatterns = [
    path("registrar/", RegistroUsuarioView.as_view(), name="registrar_usuario"), #registrar un nuevo usuario con su rol
    path('login/', LoginView.as_view(), name='login'), # inicio de sesion 
    path('cambiar-contraseña/', CambioContraseñaView.as_view(), name='cambiar-contraseña'), #cambio de contraseña

]

