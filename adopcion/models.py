from django.db import models

# Create your models here.


class Raza(models.Model):
	id_raza = models.BigAutoField(primary_key=True)
	nomb_raza = models.CharField(max_length=50)

	class Meta:
		managed = False
		db_table = 'raza'

	def __str__(self):
		return self.nomb_raza


class Animal(models.Model):
	id_animal = models.BigAutoField(primary_key=True)
	raza = models.ForeignKey(
		Raza,
		on_delete=models.DO_NOTHING,
		db_column='id_raza',
		related_name='animales',
	)
	nombre = models.CharField(max_length=50, blank=True, null=True)
	edad_aprox = models.IntegerField()
	sexo = models.CharField(max_length=15)
	peso = models.IntegerField()
	descripcion = models.CharField(max_length=150, blank=True, null=True)
	lugar_rescate = models.CharField(max_length=100)
	condicion = models.CharField(max_length=100)
	especie = models.CharField(max_length=30)
	microchip = models.BooleanField()
	foto_url = models.TextField(blank=True, null=True)
	fecha_ingreso = models.DateField()
	fecha_salida = models.DateField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'animal'

	def __str__(self):
		return self.nombre or f'{self.especie.title()} #{self.id_animal}'
