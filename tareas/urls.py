from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tareas.views.tarea_view import TareaViewSet

router = DefaultRouter()
router.register(r'tareas', TareaViewSet, basename='tarea')

urlpatterns = [
    path('', include(router.urls)),
]
