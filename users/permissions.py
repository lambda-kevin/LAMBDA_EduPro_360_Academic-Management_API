from rest_framework.permissions import BasePermission

class TienePermiso(BasePermission):
    """
    Permite acceso solo si el usuario autenticado posee el permiso requerido
    por la vista, basado en los roles asociados al usuario.
    """

    def has_permission(self, request, view):

        # 1. Verificar si la vista exige un permiso
        permiso_requerido = getattr(view, "permiso_requerido", None)

        # Si la vista no requiere permiso → acceso normal
        if not permiso_requerido:
            return True

        usuario = request.user

        # 2. Verificar autenticación
        if not usuario.is_authenticated:
            return False

        # 3. Recolectar permisos del usuario a través de sus roles
        permisos_usuario = set()

        for rol_asignado in usuario.roles_asignados.all():
            for permiso in rol_asignado.rol.permisos.all():
                permisos_usuario.add(permiso.nombre)

        # 4. Validar si el usuario posee el permiso solicitado
        return permiso_requerido in permisos_usuario
    

    

