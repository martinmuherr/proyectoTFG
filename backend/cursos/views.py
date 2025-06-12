from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from .models import Cursos, Test, CursoUsuario, Pegatina, Respuesta, Pregunta, TestResuelto, TestRespondido, Intercambio, User
from .serializers import CursosSerializer, TestSerializer, CursoUsuarioSerializer, PreguntaSerializer, PegatinaSerializer, IntercambioSerializer
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from random import choice



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuarios_mismo_curso(request):
    cursos_ids = CursoUsuario.objects.filter(user=request.user).values_list('curso_id', flat=True)
    usuarios = User.objects.filter(cursousuario__curso_id__in=cursos_ids).exclude(id=request.user.id).distinct()
    data = [{'id': u.id, 'username': u.username} for u in usuarios]
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_pegatinas(request):
    pegatinas = request.user.pegatinas.all()
    data = [{'id': p.id, 'nombre': p.nombre, 'imagen': p.imagen.url} for p in pegatinas]
    return Response(data)


class CursoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cursos.objects.all()
    serializer_class = CursosSerializer

    @action(detail=True, methods=['get'], url_path='ranking', permission_classes=[IsAuthenticated])
    def ranking(self, request, pk=None):
        curso_usuarios = CursoUsuario.objects.filter(curso__id=pk, user__profile__role='alumno').order_by('-puntos')

        vistos = set()
        data = []
        for cu in curso_usuarios:
            if cu.user.id not in vistos:
                data.append({
                    'username': cu.user.username,
                    'puntos': cu.puntos
                })
                vistos.add(cu.user.id)

        return Response(data)
    

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

        if self.request.user.is_authenticated and not self.request.user.is_staff:
            respondidos = TestRespondido.objects.filter(user=self.request.user).values_list('test_id', flat=True)
            queryset = queryset.exclude(id__in=respondidos)
            
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()] 

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='resolver', url_name='resolver')
    def resolver_test(self, request, curso_id=None, pk=None):
        if request.user.is_staff:
            return Response({'error': 'Los profesores no pueden resolver tests.'}, status=status.HTTP_403_FORBIDDEN)

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
            pegatina = Pegatina.objects.order_by('?').first()  # aleatoria
            if pegatina:
                pegatina.usuarios.add(request.user)
            curso_usuario.save()

        TestRespondido.objects.get_or_create(user=request.user, test=test)
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

class IntercambioViewSet(viewsets.ModelViewSet):
    queryset = Intercambio.objects.all()
    serializer_class = IntercambioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return Intercambio.objects.filter(receptor=self.request.user, estado='pendiente')
        return Intercambio.objects.all()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['emisor'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    @action(detail=True, methods=['patch'])
    def aceptar(self, request, pk=None):
        intercambio = self.get_object()
        pegatina_receptor_id = request.data.get('pegatina_receptor_id')
        try:
            pegatina_receptor = Pegatina.objects.get(id=pegatina_receptor_id, usuarios=request.user)
        except Pegatina.DoesNotExist:
            return Response({'error': 'Pegatina no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

        # Realizar intercambio
        intercambio.receptor.pegatinas.remove(pegatina_receptor)
        intercambio.emisor.pegatinas.remove(intercambio.pegatina_emisor)

        intercambio.receptor.pegatinas.add(intercambio.pegatina_emisor)
        intercambio.emisor.pegatinas.add(pegatina_receptor)

        intercambio.pegatina_receptor = pegatina_receptor
        intercambio.estado = 'aceptado'
        intercambio.save()
        return Response({'status': 'intercambio realizado'})

    @action(detail=True, methods=['patch'])
    def rechazar(self, request, pk=None):
        intercambio = self.get_object()
        intercambio.estado = 'rechazado'
        intercambio.save()
        return Response({'status': 'intercambio rechazado'})