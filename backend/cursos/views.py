from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import Cursos, Test, CursoUsuario, Pegatina, Respuesta, Pregunta
from .serializers import CursosSerializer, TestSerializer, CursoUsuarioSerializer, PreguntaSerializer
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CursoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cursos.objects.all()
    serializer_class = CursosSerializer




class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        curso_id = self.kwargs.get('curso_id')
        queryset = Test.objects.all()

        if curso_id:
            queryset = queryset.filter(cursos__id=curso_id)

        if not self.request.user.is_staff:
            queryset = queryset.filter(active=True)

        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()] 

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='resolver')
    def resolver_test(self, request, pk=None):
        test = self.get_object()

        if not test.active:
            return Response({'error': 'Test no está activo'}, status=status.HTTP_403_FORBIDDEN)

        respuestas_usuario = request.data.get('respuestas', {})

        correctas = 0
        for pregunta in test.preguntas.all():
            respuesta_id = respuestas_usuario.get(str(pregunta.id))
            if not respuesta_id:
                continue
            try:
                respuesta = Respuesta.objects.get(id=respuesta_id, pregunta=pregunta)
                if respuesta.correcta:
                    correctas += 1
            except Respuesta.DoesNotExist:
                continue

        if correctas == test.preguntas.count():  
            curso_usuario, _ = CursoUsuario.objects.get_or_create(
                user=request.user, curso=test.cursos
            )
            curso_usuario.puntos += 1
            pegatina = Pegatina.objects.first() 
            if pegatina:
                curso_usuario.pegatinas.add(pegatina)
            curso_usuario.save()

        return Response({'correctas': correctas, 'total': test.preguntas.count()})
    

class CursoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = CursoUsuario.objects.all()
    serializer_class = CursoUsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CursoUsuario.objects.all()
        return CursoUsuario.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PreguntasList(generics.ListAPIView):
    serializer_class = PreguntaSerializer

    def get_queryset(self):
        test_id = self.kwargs['test_id']
        return Pregunta.objects.filter(test_id=test_id)

class PreguntaUpdate(generics.UpdateAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]