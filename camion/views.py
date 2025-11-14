from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Contrato, EstadoPago
from .forms import ContratoForm, EstadoPagoForm

def crear_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save()
            messages.success(request, "Contrato creado correctamente.")
            return redirect('detalle_contrato', contrato_id=contrato.id)
    else:
        form = ContratoForm()
    return render(request, 'crear_contrato.html', {'form': form})

def detalle_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)
    estados = contrato.estados_pago.order_by('-fecha_emision')
    return render(request, 'detalle_contrato.html', {
        'contrato': contrato,
        'estados': estados
    })

def crear_estado_pago(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)
    if request.method == 'POST':
        form = EstadoPagoForm(request.POST)
        if form.is_valid():
            estado = form.save(commit=False)
            estado.contrato = contrato
            estado.save()
            messages.success(request, "Estado de pago creado correctamente.")
            return redirect('detalle_contrato', contrato_id=contrato.id)
    else:
        form = EstadoPagoForm()
    return render(request, 'crear_estado_pago.html', {
        'form': form,
        'contrato': contrato
    })

from django.shortcuts import render, get_object_or_404
from .models import Camion
from .models import EstadoPago  # si estás mostrando estados

def dashboard_camion(request, camion_id=None):
    camiones = Camion.objects.all().order_by('subcontrato')
    camion = get_object_or_404(Camion, id=camion_id) if camion_id else None

    estados_pago = EstadoPago.objects.filter(camion=camion).order_by('-fecha_inicio') if camion else []

    resumen_estados = []
    if not camion:
        resumen_estados = EstadoPago.objects.select_related('camion').order_by('-fecha_inicio')

    return render(request, 'dashboard_camion.html', {
        'camiones': camiones,
        'camion': camion,
        'estados_pago': estados_pago,
        'resumen_estados': resumen_estados
    })

from django.shortcuts import render
from .models import Camion

def listar_camion(request):
    camion = Camion.objects.all().order_by('subcontrato')
    return render(request, 'listar_camion.html', {
        'camiones': camion
    })

from django.shortcuts import render, redirect
from .forms import CamionForm
from django.contrib import messages

def crear_camion(request):
    if request.method == 'POST':
        form = CamionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Camión creado correctamente.")
            return redirect('listar_camiones')  # o donde quieras redirigir
    else:
        form = CamionForm()
    return render(request, 'camion.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .forms import EstadoPagoCompletoForm
from .models import Camion, EstadoPago

def crear_estado_pago_completo(request, camion_id):
    camion = get_object_or_404(Camion, id=camion_id)

    if request.method == 'POST':
        form = EstadoPagoCompletoForm(request.POST)
        if form.is_valid():
            estado = form.save(commit=False)
            estado.camion = camion
            estado.save()
            return redirect('dashboard_camion')  # o donde quieras redirigir
    else:
        form = EstadoPagoCompletoForm()

    return render(request, 'crear_estado_pago_completo.html', {
        'form': form,
        'camion': camion
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Camion
from .forms import CamionForm

def editar_camion(request, camion_id):
    camion = get_object_or_404(Camion, id=camion_id)

    if request.method == 'POST':
        form = CamionForm(request.POST, instance=camion)
        if form.is_valid():
            form.save()
            return redirect('dashboard_camion', camion_id=camion.id)
    else:
        form = CamionForm(instance=camion)

    return render(request, 'editar_camion.html', {
        'form': form,
        'camion': camion
    })

from django.shortcuts import get_object_or_404, redirect
from .models import Camion

def eliminar_camion(request, camion_id):
    camion = get_object_or_404(Camion, id=camion_id)
    camion.delete()
    return redirect('dashboard_camion')

from django.shortcuts import render
from .models import EstadoPago

def ver_estados_pago(request):
    estados = EstadoPago.objects.select_related('camion').order_by('-fecha_inicio')
    return render(request, 'ver_estados_pago.html', {
        'estados': estados
    })

from django.shortcuts import render, get_object_or_404
from .models import EstadoPago

def detalle_estado_pago(request, estado_id):
    estado = get_object_or_404(EstadoPago, id=estado_id)
    return render(request, 'detalle_estado_pago.html', {
        'estado': estado
    })

from django.db.models import Count
from .models import EstadoPago

def detalle_estado_pago(request, estado_id):
    estado = get_object_or_404(EstadoPago, id=estado_id)
    numero_estado = EstadoPago.objects.filter(camion=estado.camion, fecha_termino__lte=estado.fecha_termino).count()
    return render(request, 'detalle_estado_pago.html', {
        'estado': estado,
        'numero_estado': numero_estado
    })