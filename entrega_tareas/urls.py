from django.urls import path, include
from rest_framework.routers import DefaultRouter
from entrega_tareas.views.entrega_view import EntregaTareaViewSet

router = DefaultRouter()
router.register(r'entregas', EntregaTareaViewSet, basename='entrega')

urlpatterns = [
    path('', include(router.urls)),
]
