from rest_framework import viewsets
from entrega_tareas.models import EntregaTarea
from entrega_tareas.serializers.entrega_serializer import EntregaTareaSerializer
from entrega_tareas.permissions import IsEstudiante, IsStaffEntrega, IsEstudianteOrStaffEntrega

class EntregaTareaViewSet(viewsets.ModelViewSet):
    queryset = EntregaTarea.objects.all()
    serializer_class = EntregaTareaSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsEstudiante()]  # solo estudiante entrega
        if self.action in ['list', 'retrieve']:
            return [IsEstudianteOrStaffEntrega()]  # estudiantes ven solo lo suyo, docentes ven sus asignaturas
        return [IsStaffEntrega()]  # update/delete → staff solo

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'rol') and user.rol == 'estudiante':
            return EntregaTarea.objects.filter(estudiante=user)
        if hasattr(user, 'rol') and user.rol in ['docente', 'administrador', 'coordinador']:
            return EntregaTarea.objects.filter(tarea__asignatura__docente_id=user.id)
        return EntregaTarea.objects.none()
