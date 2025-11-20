from rest_framework import permissions

class IsDocente(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol docente.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'rol') and request.user.rol == 'docente'
