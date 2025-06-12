from rest_framework import serializers
from .models import Cursos, Test, Pregunta, Respuesta, CursoUsuario, Pegatina, Intercambio

class CursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursos
        fields = ['id', 'name']

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['id', 'texto']

class PreguntaSerializer(serializers.ModelSerializer):
    respuestas = RespuestaSerializer(many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = ['id', 'texto', 'respuestas', 'active'] 


class TestSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'name', 'content', 'active', 'preguntas']

class PegatinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pegatina
        fields = ['id', 'nombre', 'imagen']

class CursoUsuarioSerializer(serializers.ModelSerializer):
    pegatinas = PegatinaSerializer(many=True, read_only=True)

    class Meta:
        model = CursoUsuario
        fields = ['id', 'user', 'curso', 'puntos', 'pegatinas']


class IntercambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intercambio
        fields = '__all__'

