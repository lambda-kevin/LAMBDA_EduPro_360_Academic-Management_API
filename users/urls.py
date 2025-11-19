from django.urls import path

from users.views.registro_view import RegistroUsuarioView
from users.views.inicio_sesion_view import LoginView
from users.views.cambio_contrasena_view import CambioContraseñaView
from users.views.recuperacion_contrasena_view import (
    SolicitarRecuperacionView,
    ValidarTokenView,
    RestablecerContraseñaView
)

from users.views.roles_view import (
    CrearPermisoView,
    ListaPermisosView,
    CrearRolView,
    ListaRolesView,
    AsignarPermisoRolView,
    AsignarRolUsuarioView,
    RolesDeUsuarioView,
    RemoverRolUsuarioView
)

urlpatterns = [
    # =========================================
    # USUARIO
    # =========================================
    path("registrar/", RegistroUsuarioView.as_view(), name="registrar_usuario"),
    path("login/", LoginView.as_view(), name="login"),
    path("cambiar-contraseña/", CambioContraseñaView.as_view(), name="cambiar_contraseña"),

    # =========================================
    # RECUPERACIÓN DE CONTRASEÑA
    # =========================================
    path("solicitar-recuperacion/", SolicitarRecuperacionView.as_view(), name="solicitar_recuperacion"),
    path("validar-token/", ValidarTokenView.as_view(), name="validar_token"),
    path("restablecer-contraseña/", RestablecerContraseñaView.as_view(), name="restablecer_contraseña"),

    # =========================================
    # PERMISOS
    # =========================================
    path("permisos/crear/", CrearPermisoView.as_view(), name="crear_permiso"),
    path("permisos/", ListaPermisosView.as_view(), name="lista_permisos"),

    # =========================================
    # ROLES
    # =========================================
    path("roles/crear/", CrearRolView.as_view(), name="crear_rol"),
    path("roles/", ListaRolesView.as_view(), name="lista_roles"),
    path("roles/asignar-permiso/", AsignarPermisoRolView.as_view(), name="asignar_permiso_rol"),

    # =========================================
    # ROLES DE USUARIOS
    # =========================================
    path("usuarios/asignar-rol/", AsignarRolUsuarioView.as_view(), name="asignar_rol_usuario"),
    path("usuarios/<int:usuario_id>/roles/", RolesDeUsuarioView.as_view(), name="roles_de_usuario"),
    path("usuarios/remover-rol/", RemoverRolUsuarioView.as_view(), name="remover_rol_usuario"),
]
