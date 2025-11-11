from django.shortcuts import render
from django.shortcuts import render, redirect

from .models import FacturaCompra
from .utils import leer_facturas_desde_archivo  # Asegúrate de tener

def subir_libro_sii(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        fecha_libro = request.POST.get('fecha_libro')

        facturas_actualizadas = 0
        facturas_creadas = 0

        for factura in leer_facturas_desde_archivo(archivo):
            folio = factura['folio'].strip().lstrip('0')
            existente = FacturaCompra.objects.filter(folio__iexact=folio).first()

            if existente:
                existente.monto_exento = factura['monto_exento']
                existente.monto_neto = factura['monto_neto']
                existente.monto_iva = factura['monto_iva']
                existente.monto_total = factura['monto_total']
                existente.save()
                facturas_actualizadas += 1
            else:
                FacturaCompra.objects.create(
                    folio=folio,
                    fecha_emision=factura['fecha_emision'],
                    proveedor=factura['proveedor'],
                    rut_proveedor=factura['rut_proveedor'],
                    monto_exento=factura['monto_exento'],
                    monto_neto=factura['monto_neto'],
                    monto_iva=factura['monto_iva'],
                    monto_total=factura['monto_total'],
                    pagada=False,
                    origen_libro=fecha_libro
                )
                facturas_creadas += 1

        print(f"Actualizadas: {facturas_actualizadas}, Nuevas: {facturas_creadas}")
        return redirect('listar_facturas')

    return render(request, 'subir_libro.html')

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.db.models import Sum
from .models import FacturaCompra

def listar_facturas(request):
    facturas = FacturaCompra.objects.all().order_by('-fecha_emision')

    # Filtros
    mes = request.GET.get('mes')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    rut = request.GET.get('rut')
    folio = request.GET.get('folio')
    estado = request.GET.get('estado')

    if mes:
        try:
            mes_dt = datetime.strptime(mes, '%Y-%m')
            facturas = facturas.filter(
                fecha_emision__year=mes_dt.year,
                fecha_emision__month=mes_dt.month
            )
        except ValueError:
            pass

    if fecha_inicio and fecha_fin:
        try:
            inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            facturas = facturas.filter(fecha_emision__range=(inicio_dt, fin_dt))
        except ValueError:
            pass

    if rut:
        facturas = facturas.filter(rut_proveedor__icontains=rut)

    if folio:
        facturas = facturas.filter(folio__icontains=folio)

    if estado == 'pendiente':
        facturas = facturas.filter(pagada=False)
    elif estado == 'pagada':
        facturas = facturas.filter(pagada=True)

    # Total filtrado
    total_filtrado = facturas.aggregate(total=Sum('monto_total'))['total'] or 0

    # Procesar cambios
    if request.method == 'POST':
        seleccionadas = request.POST.getlist('factura_id')
        folio_desbloqueo = request.POST.get('folio_desbloqueo', '').strip()
        clave_desbloqueo = request.POST.get('clave_desbloqueo', '').strip()
        clave_correcta = "DESBLOQUEAR2025"

        for factura in facturas:
            file_field = f'comprobante_{factura.id}'
            if file_field in request.FILES:
                factura.comprobante = request.FILES[file_field]

            if factura.pagada:
                if str(factura.id) not in seleccionadas and factura.folio == folio_desbloqueo and clave_desbloqueo == clave_correcta:
                    factura.pagada = False
                    factura.fecha_pago = None
            else:
                if str(factura.id) in seleccionadas:
                    factura.pagada = True
                    factura.fecha_pago = timezone.now().date()

            factura.save()

        return redirect(request.get_full_path())

    return render(request, 'listar_facturas.html', {
        'facturas': facturas,
        'mes_seleccionado': mes,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'rut': rut,
        'folio': folio,
        'estado': estado,
        'total_filtrado': total_filtrado,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import FacturaCompra

def pagar_factura(request, factura_id):
    factura = get_object_or_404(FacturaCompra, id=factura_id)

    if factura.pagada:
        return render(request, 'pagar_factura.html', {
            'factura': factura,
            'mensaje': 'Esta factura ya está marcada como pagada.',
        })

    if request.method == 'POST':
        factura.pagada = True
        factura.fecha_pago = timezone.now().date()
        factura.save()
        return redirect('listar_facturas')

    return render(request, 'pagar_factura.html', {'factura': factura})

from django.shortcuts import render, redirect
from .models import FacturaCompra
from .utils import leer_facturas_desde_archivo  # usa la misma función que ya tienes

def actualizar_montos_facturas(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        actualizadas = 0
        no_encontradas = []

        for factura in leer_facturas_desde_archivo(archivo):
            folio = factura['folio'].strip().lstrip('0')  # normaliza el folio
            try:
                obj = FacturaCompra.objects.get(folio__iexact=folio)
                obj.monto_exento = factura['monto_exento']
                obj.monto_neto = factura['monto_neto']
                obj.monto_iva = factura['monto_iva']
                obj.monto_total = factura['monto_total']
                obj.save()
                actualizadas += 1
            except FacturaCompra.DoesNotExist:
                no_encontradas.append(folio)

        context = {
            'actualizadas': actualizadas,
            'no_encontradas': no_encontradas,
        }
        return render(request, 'resultado_actualizacion.html', context)

    return render(request, 'subir_actualizacion_montos.html')