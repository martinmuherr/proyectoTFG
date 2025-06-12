from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CursoViewSet, TestViewSet, CursoUsuarioViewSet, PreguntasList, PreguntaUpdate, IntercambioViewSet, usuarios_mismo_curso
from . import views


router = DefaultRouter()
router.register(r'intercambios', IntercambioViewSet, basename='intercambio')
router.register(r'usuarios-curso', CursoUsuarioViewSet)
router.register(r'(?P<curso_id>\d+)/tests', TestViewSet, basename='curso-tests')
router.register(r'', CursoViewSet)


urlpatterns = [
    path('tests/<int:test_id>/preguntas/', PreguntasList.as_view(), name='preguntas-list'),
    path('preguntas/<int:pk>/', PreguntaUpdate.as_view(), name='pregunta-update'),
    path('mis-pegatinas/', views.mis_pegatinas, name='mis_pegatinas'),
    path('usuarios-mismo-curso/', usuarios_mismo_curso, name='usuarios_mismo_curso'),
    path('historial-intercambios/', views.historial_intercambios, name='historial_intercambios'),
    path('', include(router.urls)),
]
