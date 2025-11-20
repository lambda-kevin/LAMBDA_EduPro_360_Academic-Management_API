from rest_framework import permissions

class IsEstudiante(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol estudiante.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'rol') and request.user.rol == 'estudiante'


class IsStaffEntrega(permissions.BasePermission):
    """
    Permite acceso a usuarios con rol docente, administrador o coordinador.
    """
    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'rol') and 
            request.user.rol in ['docente', 'administrador', 'coordinador']
        )


class IsEstudianteOrStaffEntrega(permissions.BasePermission):
    """
    Permite acceso si el usuario es estudiante O staff de entrega.
    """
    def has_permission(self, request, view):
        return (
            IsEstudiante().has_permission(request, view)
            or
            IsStaffEntrega().has_permission(request, view)
        )
