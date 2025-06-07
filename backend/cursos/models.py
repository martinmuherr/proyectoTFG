from django.db import models
from django.contrib.auth.models import User

class Cursos(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Test(models.Model):
    name = models.CharField(max_length=100)
    content = models.JSONField()  # Guarda el JSON con las preguntas/respuestas
    active = models.BooleanField(default=False)
    cursos = models.ForeignKey(Cursos, on_delete=models.CASCADE, related_name='tests')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # profesor que creó/activó

    def __str__(self):
        return self.name

class CursoUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Cursos, on_delete=models.CASCADE)
    puntos = models.PositiveIntegerField(default=0)
    pegatinas = models.ManyToManyField('Pegatina', blank=True)

    class Meta:
        unique_together = ('user', 'curso')

    def __str__(self):
        return f"{self.user.username} - {self.curso.name}"
        
class Pegatina(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='pegatinas/')

    def __str__(self):
        return self.nombre
    
class Pregunta(models.Model):
    test = models.ForeignKey('Test', related_name='preguntas', on_delete=models.CASCADE)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='respuestas', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    correcta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texto} ({'Correcta' if self.correcta else 'Incorrecta'})"