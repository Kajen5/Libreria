from django.urls import path
from . import views

app_name = 'autos'
urlpatterns = [
    path('', views.index.as_view(), name='Index'),
    path('reserva/<str:matricula>', views.reservaView, name='Reserva'),
    path('reserva/<str:matriculapost>/registro', views.registrarReserva, name='ReservaPost')
]
