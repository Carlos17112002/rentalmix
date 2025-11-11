from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Camion

from django.db.models import Sum
from .models import Camion, EstadoPagoCamion

def dashboard_camiones(request, camion_id=None):
    camiones = Camion.objects.all().order_by('patente')
    camion = Camion.objects.filter(id=camion_id).first() if camion_id else None

    resumen = []
    for c in camiones:
        total_pagado = EstadoPagoCamion.objects.filter(camion=c).aggregate(total=Sum('total_a_pagar'))['total'] or 0
        resumen.append({
            'camion': c,
            'total_pagado': total_pagado
        })

    estados = EstadoPagoCamion.objects.filter(camion=camion).order_by('-fecha_emision') if camion else []

    return render(request, 'dashboard_camiones.html', {
        'camiones': camiones,
        'camion': camion,
        'estados': estados,
        'resumen': resumen
    })

from django.shortcuts import render, redirect
from .forms import CamionForm
from .models import Camion

def agregar_camion(request):
    if request.method == 'POST':
        form = CamionForm(request.POST)
        if form.is_valid():
            nuevo_camion = form.save()
            return redirect('camion_detalle', camion_id=nuevo_camion.id)
    else:
        form = CamionForm()
    return render(request, 'agregar_camion.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Camion, EstadoPagoCamion, ArriendoCamion, Contrato

def camion_detalle(request, camion_id):
    camion = get_object_or_404(Camion, id=camion_id)
    contratos = Contrato.objects.filter(camion=camion).order_by('-fecha_inicio')
    return render(request, 'camion_detalle.html', {
        'camion': camion,
        'contratos': contratos
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from .models import Contrato, Camion

def crear_contrato(request, camion_id=None):
    camion = get_object_or_404(Camion, id=camion_id) if camion_id else None
    camiones = Camion.objects.all() if not camion else None

    if request.method == 'POST':
        # Obtener datos del formulario
        camion_id_post = request.POST.get('camion') or (camion.id if camion else None)
        nombre = request.POST.get('nombre')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_termino = request.POST.get('fecha_termino')
        valor_dia = request.POST.get('valor_dia')

        # Validaciones básicas
        if not (camion_id_post and nombre and fecha_inicio and fecha_termino and valor_dia):
            messages.error(request, "Completa todos los campos.")
            return redirect(request.path)

        camion_obj = get_object_or_404(Camion, id=camion_id_post)
        fecha_inicio = date.fromisoformat(fecha_inicio)
        fecha_termino = date.fromisoformat(fecha_termino)

        if fecha_termino < fecha_inicio:
            messages.error(request, "La fecha de término no puede ser anterior a la de inicio.")
            return redirect(request.path)

        # Crear contrato
        contrato = Contrato.objects.create(
            camion=camion_obj,
            nombre=nombre,
            fecha_inicio=fecha_inicio,
            fecha_termino=fecha_termino,
            valor_dia=int(valor_dia)
        )

        messages.success(request, "Contrato creado correctamente.")
        return redirect('camion_detalle', camion_id=camion_obj.id)

    return render(request, 'crear_contrato.html', {
        'camion': camion,
        'camiones': camiones
    })

from django.shortcuts import render, get_object_or_404
from .models import Contrato

def detalle_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)
    return render(request, 'detalle_contrato.html', {
        'contrato': contrato
    })