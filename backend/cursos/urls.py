from rest_framework.routers import DefaultRouter
from .views import CursoViewSet, TestViewSet, CursoUsuarioViewSet

router = DefaultRouter()
router.register(r'usuarios-curso', CursoUsuarioViewSet)
router.register(r'', CursoViewSet)
router.register(r'(?P<curso_id>\d+)/tests', TestViewSet, basename='curso-tests')

urlpatterns = router.urls
