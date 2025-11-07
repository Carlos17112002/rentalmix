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
from .models import Camion, EstadoPagoCamion, ArriendoCamion

def camion_detalle(request, camion_id):
    camion = get_object_or_404(Camion, id=camion_id)
    estados = EstadoPagoCamion.objects.filter(camion=camion).order_by('-fecha_emision')
    arriendos = ArriendoCamion.objects.filter(camion=camion).order_by('-fecha_inicio')

    if request.method == 'POST' and 'periodo' in request.POST:
        # Captura de datos
        presente = int(request.POST.get('presente_estado_pago', 0))
        devolucion = int(request.POST.get('devolucion_anticipo', 0))
        multas = int(request.POST.get('descuentos_multas', 0))
        seguro = int(request.POST.get('devolucion_seguro', 0))
        descuento_pct = float(request.POST.get('descuento_especial', 0))

        subtotal = presente - devolucion - multas + seguro
        subtotal_con_descuento = int(subtotal - (subtotal * descuento_pct / 100))
        iva = int(subtotal_con_descuento * 0.19)
        total_estado = subtotal_con_descuento + iva

        retencion = int(request.POST.get('retencion', 0))
        devolucion_retenciones = int(request.POST.get('devolucion_retenciones', 0))
        saldo_anterior_retenciones = int(request.POST.get('saldo_anterior_retenciones', 0))
        nuevo_saldo_retenciones = saldo_anterior_retenciones + retencion - devolucion_retenciones

        total_pagar = total_estado - retencion

        EstadoPagoCamion.objects.create(
            camion=camion,
            periodo=request.POST.get('periodo'),
            anticipo=int(request.POST.get('anticipo', 0)),
            avance_a_la_fecha=int(request.POST.get('avance_a_la_fecha', 0)),
            estado_pago_anterior=int(request.POST.get('estado_pago_anterior', 0)),
            presente_estado_pago=presente,
            devolucion_anticipo=devolucion,
            descuentos_multas=multas,
            saldo_anterior_anticipo=int(request.POST.get('saldo_anterior_anticipo', 0)),
            devolucion_seguro=seguro,
            nuevo_saldo_anticipo=seguro,  # si es igual a devolución
            subtotal=subtotal,
            descuento_especial=descuento_pct,
            subtotal_con_descuento=subtotal_con_descuento,
            iva=iva,
            total_estado_pago=total_estado,
            saldo_anterior_retenciones=saldo_anterior_retenciones,
            retencion=retencion,
            devolucion_retenciones=devolucion_retenciones,
            nuevo_saldo_retenciones=nuevo_saldo_retenciones,
            total_a_pagar=total_pagar
        )
        return redirect('camion_detalle', camion_id=camion.id)

    return render(request, 'camion_detalle.html', {
        'camion': camion,
        'estados': estados,
        'arriendos': arriendos,
        'form_arriendo': None
    })