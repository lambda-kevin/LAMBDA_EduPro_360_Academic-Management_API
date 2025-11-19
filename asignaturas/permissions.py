from rest_framework.permissions import BasePermission

class PuedeVerAsignaturas(BasePermission):
    """
    Permite acceder solo a usuarios que tengan el permiso 'crear_asignatura'
    o el permiso que yo quiero validar.
    """
    def has_permission(self, request, view):
        return request.user and request.user.has_perm('users.crear_asignatura')
