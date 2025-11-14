from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),

    # Endpoints de la app users (login, update, roles, permisos)
    path('api/users/', include('users.urls')),
    path('api/auth/', include('rest_framework.urls')),


    # Documentación de la API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
