from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    UserUpdateView,
    RoleViewSet,
    PermissionListView,
    UserRoleAssignView
)

# Usamos router para los endpoints de roles (ModelViewSet)
router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='roles')

urlpatterns = [
    # LOGIN y renovación de token
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # Actualizar usuario (solo admins)
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),

    # Endpoint para listar permisos
    path('permissions/', PermissionListView.as_view(), name='permissions_list'),

    # Endpoint para asignar roles a un usuario
    path('assign-roles/<int:pk>/', UserRoleAssignView.as_view(), name='user_assign_roles'),

    # Incluimos el router para CRUD completo de roles
    path('', include(router.urls)),
]
