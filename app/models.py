from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Usuario(models.Model):
    user = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    tlf = models.CharField(max_length=12)
    mail = models.CharField(max_length=50)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.nombre


class Tarea(models.Model):
    nombre = models.CharField(max_length=200)
    prioridad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    fecha_vencimiento = models.DateField()
    estado = models.BooleanField(default=False)
    usuarios = models.ManyToManyField(Usuario)

    def cambiar_estado(self, usuario):
        # Verificar si el usuario está asociado a la tarea
        if usuario in self.usuarios.all():
            # Cambiar el estado de la tarea
            self.estado = not self.estado
            self.save()
            return True
        return False

    def obtener_nombres_usuarios(self):
        return ", ".join([usuario.nombre for usuario in self.usuarios.all()])
