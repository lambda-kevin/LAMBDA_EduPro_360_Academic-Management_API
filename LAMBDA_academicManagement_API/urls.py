from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    # Rutas del módulo de usuarios
    path('api/users/', include('users.urls')), 
    path('api/asignaturas/', include('asignaturas.urls')),  
    path('api/tareas/', include('tareas.urls')),   



    # (Opcional) rutas de autenticación
    path('api/auth/', include('rest_framework.urls')),
]

