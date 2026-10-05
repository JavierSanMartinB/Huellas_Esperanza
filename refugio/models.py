from django.db import models

# Create your models here.

class Usuario (models.Model):
    usuario_id = models.BigAutoField(primary_key=True)
    nomb = models.CharField(max_length=50)
    ap_paterno = models.CharField(max_length=50)
    ap_materno = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50, unique=True, blank=True, null=True)
    fecha_nac = models.DateField()
    direccion = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    contrasena_hash = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nomb} {self.ap_paterno} {self.ap_materno}"


class Refugio(models.Model):
    id_refugio = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=100)
    descripcion = models.TextField()
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'refugio'

    def __str__(self):
        return self.nombre