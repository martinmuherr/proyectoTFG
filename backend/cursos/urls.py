from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CursoViewSet, TestViewSet, CursoUsuarioViewSet, PreguntasList, PreguntaUpdate
from . import views


router = DefaultRouter()
router.register(r'usuarios-curso', CursoUsuarioViewSet)
router.register(r'', CursoViewSet)
router.register(r'(?P<curso_id>\d+)/tests', TestViewSet, basename='curso-tests')

urlpatterns = [
    path('tests/<int:test_id>/preguntas/', PreguntasList.as_view(), name='preguntas-list'),
    path('preguntas/<int:pk>/', PreguntaUpdate.as_view(), name='pregunta-update'),
    path('mis-pegatinas/', views.mis_pegatinas, name='mis_pegatinas'),
    path('', include(router.urls)),
]
