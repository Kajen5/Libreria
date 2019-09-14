from django.db import models
from django.forms import ModelForm, DateInput
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils import timezone
from os import path


class gama(models.Model):
    id_gama = models.CharField(max_length=10, primary_key=True)
    descripcion = models.CharField(max_length=60)

    def __str__(self):
        return self.id_gama


class Vehiculos(models.Model):
    Choices_motor = (
        'Diesel',
        'Gasolina',
        'Electrico'
    )
    Choices_vehiculos = (
        'Turismo',
        'Deportivo',
        'Camion',
        'Limosina',
        'Monovulemen'
    )
    matricula = models.CharField(max_length=7, primary_key=True)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    tipo_motor = models.IntegerField(choices=enumerate(Choices_motor))
    tipo_vehiculo = models.IntegerField(choices=enumerate(Choices_vehiculos))
    descripcion = models.CharField(max_length=20)
    techo_electrico = models.BooleanField()
    climatizacion = models.BooleanField()
    interior_cuero = models.BooleanField()
    stma_navegacion = models.BooleanField()
    cambio_automatico = models.BooleanField()
    gama = models.ForeignKey(gama, on_delete=models.PROTECT)
    tarifa_dia = models.DecimalField(
        default=0, max_digits=10, decimal_places=2)
    imagen = models.ImageField(
        upload_to='cars/', default='carro.png')

    def __str__(self):
        return self.matricula 

    class Meta:
        verbose_name_plural = "Vehiculos"


class usuarios(User):
    username_validator = ASCIIUsernameValidator()

    class Meta:
        proxy = True
        verbose_name_plural = "Usuarios"


class reserva(models.Model):
    id_usuario = models.ForeignKey(usuarios, on_delete=models.PROTECT)
    dia_recogida = models.DateField(unique=True)
    dia_entrega = models.DateField(unique=True)
    matricula = models.ForeignKey(Vehiculos, on_delete=models.PROTECT)
    precio = models.DecimalField(
        default=0, max_digits=10, decimal_places=2)

    def dias(self):
        return (self.dia_entrega - self.dia_recogida).days + 1

    def __str__(self):
        return str(self.id) + " = " + str(self.dia_recogida) + " --> " + str(self.dia_entrega) + "  (" + str(self.matricula) + ")"

    class Meta:
        verbose_name_plural = "Reservas"

class vehiculoForm(ModelForm):
    class Meta:
        model = Vehiculos
        fields = [
            'tipo_motor',
            'tipo_vehiculo',
            'techo_electrico', 'climatizacion',
            'interior_cuero', 'stma_navegacion',
            'cambio_automatico'
        ]


class datecustome(DateInput):
    input_type = 'date'

class reservaForm(ModelForm):
    class Meta:
        model = reserva
        fields = [
            'dia_recogida',
            'dia_entrega'
        ]
        widgets = {
            'dia_recogida': datecustome(),
            'dia_entrega': datecustome()
        }
