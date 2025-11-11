from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Camion

from django.shortcuts import render, get_object_or_404
from .models import Camion, Contrato

def dashboard_camiones(request, camion_id=None):
    camiones = Camion.objects.all().order_by('patente')
    camion = get_object_or_404(Camion, id=camion_id) if camion_id else None

    # Contratos del camión seleccionado
    contratos = Contrato.objects.filter(camion=camion).order_by('-fecha_inicio') if camion else []

    # Resumen general de contratos si no hay camión seleccionado
    resumen_contratos = []
    if not camion:
        for contrato in Contrato.objects.select_related('camion').order_by('-fecha_inicio'):
            resumen_contratos.append({
                'contrato': contrato,
                'camion': contrato.camion,
                'dias': contrato.dias_arriendo,
                'total': contrato.total_arriendo
            })

    return render(request, 'dashboard_camiones.html', {
        'camiones': camiones,
        'camion': camion,
        'contratos': contratos,
        'resumen_contratos': resumen_contratos
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

def editar_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)
    if request.method == 'POST':
        contrato.nombre = request.POST.get('nombre')
        contrato.fecha_inicio = request.POST.get('fecha_inicio')
        contrato.fecha_termino = request.POST.get('fecha_termino')
        contrato.valor_dia = int(request.POST.get('valor_dia'))
        contrato.save()
        return redirect('detalle_contrato', contrato_id=contrato.id)
    return render(request, 'editar_contratos.html', {
        'contrato': contrato
    })

def eliminar_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)
    camion_id = contrato.camion.id
    contrato.delete()
    return redirect('camion_detalle', camion_id=camion_id)