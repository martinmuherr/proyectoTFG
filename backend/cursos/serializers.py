from rest_framework import serializers
from .models import Cursos, Test, Pregunta, Respuesta, CursoUsuario, Pegatina

class CursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursos
        fields = ['id', 'name']

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'name', 'content', 'active', 'cursos', 'created_by']
        read_only_fields = ['created_by']

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['id', 'texto']


class PreguntaSerializer(serializers.ModelSerializer):
    respuestas = RespuestaSerializer(many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = ['id', 'enunciado', 'respuestas']


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