from django.urls import path
from .views import RegistroUsuarioView
from .views import LoginView

urlpatterns = [
    path("registrar/", RegistroUsuarioView.as_view(), name="registrar_usuario"),
    path('login/', LoginView.as_view(), name='login')
]
