from django.contrib import admin
from .models import Cursos, Test, Pregunta, Respuesta

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

admin.site.register(Cursos)
admin.site.register(Test, TestAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Respuesta)
