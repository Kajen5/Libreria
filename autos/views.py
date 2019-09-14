from django.shortcuts import render
from django.views import generic
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime


class index(generic.ListView):
    template_name = "autos/index.html"
    context_object_name = 'latest_question_list'
    paginate_by = 10

    def get_queryset(self):
        """Return the last five published questions."""
        return Vehiculos.objects.all().order_by("tarifa_dia")


def reservaView(request, matricula):
    if request.user.is_authenticated:
        context = {
            'form': reservaForm(),
            'vehiculo': Vehiculos.objects.get(matricula=matricula)}
        return render(request, 'autos/reserva.html', context)
    else:
        context = {
            'notform': 'Es necesario autentificar el usuario'}
        return render(request, 'autos/reserva.html', context)


def registrarReserva(request, matriculapost):
    vehiculo = Vehiculos.objects.get(matricula=matriculapost)
    if not request.user.is_authenticated:
        context = {'notform': 'Es necesario autentificar el usuario'}
        return render(request, 'autos/reserva.html', context)
    form = reservaForm(request.POST or None)
    context2 = {
        'form': reservaForm(),
        'vehiculo': vehiculo}
    h = None
    fecha_desde = fecha_hasta = datetime.datetime.strptime(
        request.POST['dia_recogida'], '%Y-%m-%d').date()
    fecha_hasta = fecha_hasta = datetime.datetime.strptime(
        request.POST['dia_entrega'], '%Y-%m-%d').date()
    base = reserva.objects.filter(matricula=matriculapost)
    h = base.filter(dia_recogida__range=(fecha_desde, fecha_hasta))
    h |= base.filter(dia_entrega__range=(fecha_desde, fecha_hasta))
    for i in base:
        if i.dia_recogida <= fecha_hasta <= i.dia_entrega:
            h |= base.filter(pk=i.pk)
    h |= base.filter(dia_recogida=fecha_hasta)
    h |= base.filter(dia_entrega=fecha_desde)
    if not form.is_valid():
        context2['error_message'] = "manipulacion de datos no autorizada, informacion introducida no valido"
        context2['dia_a'] = fecha_desde
        context2['dia_b'] = fecha_hasta
        if h.count() is not 0:
            context2['h'] = h.order_by('dia_recogida').distinct()
        return render(request, 'autos/reserva.html', context2)
    fecha_desde = form.cleaned_data['dia_recogida']
    fecha_hasta = form.cleaned_data['dia_entrega']
    dias = fecha_hasta - fecha_desde
    if (dias.days < 0):
        print(dias)
        context2['error_message'] = "fecha no concuerda"
        return render(request, 'autos/reserva.html', context2)
    if h.count() is not 0:
        context2['error_message'] = "ya esta recervado el vehiculo entre las fechas pedidas"
        context2['h'] = h.order_by('dia_recogida').distinct()
        context2['dia_a'] = fecha_desde
        context2['dia_b'] = fecha_hasta
        return render(request, 'autos/reserva.html', context2)
    p = reserva(
        id_usuario=request.user,
        dia_recogida=fecha_desde,
        dia_entrega=fecha_hasta,
        matricula=vehiculo,
        precio=vehiculo.tarifa_dia * (dias.days + 1))
    context = {
        "reserva": p,
        "vehiculo": vehiculo
    }

    p.save()
    print("hola")
    print(p.id)
    return render(request, 'autos/reserva_success.html', context)
