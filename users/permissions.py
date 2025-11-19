from rest_framework.permissions import BasePermission

class TienePermiso(BasePermission):
    def has_permission(self, request, view):
        permiso_requerido = getattr(view, "permiso_requerido", None)

        if not permiso_requerido:
            return True

        usuario = request.user

        # usuario no logueado
        if not usuario.is_authenticated:
            return False

        # traer permisos por los roles del usuario
        permisos_usuario = set()
        for rol in usuario.roles_asignados.all():
            permisos_usuario.update(perm.nombre for perm in rol.rol.permisos.all())

        return permiso_requerido in permisos_usuario
