from django.contrib import admin
from .models import Cursos, Test, Pregunta, Respuesta, Pegatina, CursoUsuario, Intercambio, User
from .forms import IntercambioForm

class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1

class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'cursos')
    inlines = [PreguntaInline]

class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 1

class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'test')
    inlines = [RespuestaInline]

@admin.register(Pegatina)
class PegatinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'imagen')

@admin.register(CursoUsuario)
class CursoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'curso', 'puntos')
    filter_horizontal = ('pegatinas',)

@admin.register(Intercambio)
class IntercambioAdmin(admin.ModelAdmin):
    form = IntercambioForm
    list_display = ('emisor', 'receptor', 'pegatina_emisor', 'pegatina_receptor', 'estado', 'creado')
    raw_id_fields = ('emisor', 'receptor')



admin.site.register(Cursos)
admin.site.register(Test, TestAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Respuesta)
