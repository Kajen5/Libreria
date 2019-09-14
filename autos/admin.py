from django.contrib import admin
from .models import *


class ReservaInline(admin.TabularInline):
    model = reserva

class VehiculosAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'marca',
                    'modelo', 'tipo_motor',
                    'tipo_vehiculo', 'descripcion',
                    'techo_electrico', 'climatizacion',
                    'interior_cuero', 'stma_navegacion',
                    'cambio_automatico')
    list_filter = ('tipo_motor',
                    'tipo_vehiculo',
                    'techo_electrico', 'climatizacion',
                    'interior_cuero', 'stma_navegacion',
                    'cambio_automatico')
    search_fields = ['matricula', 'marca',
                        'modelo']
    inlines = [ReservaInline]


admin.site.register(Vehiculos, VehiculosAdmin)
admin.site.register((gama, usuarios, reserva))


# Register your models here.
