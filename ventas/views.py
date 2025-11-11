from django.shortcuts import render, redirect
from .models import LibroVenta, FacturaVenta
from .utils import leer_ventas_desde_archivo
from datetime import datetime


from .utils import leer_ventas_desde_archivo

def subir_libro_ventas(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        fecha_libro = request.POST.get('fecha_libro')

        actualizadas = 0
        creadas = 0

        for venta in leer_ventas_desde_archivo(archivo):
            folio = venta['folio'].strip().lstrip('0')
            obj = FacturaVenta.objects.filter(folio__iexact=folio).first()

            if obj:
                obj.monto_exento = venta['monto_exento']
                obj.monto_neto = venta['monto_neto']
                obj.monto_iva = venta['monto_iva']
                obj.monto_total = venta['monto_total']
                obj.save()
                actualizadas += 1
            else:
                FacturaVenta.objects.create(
                    folio=folio,
                    fecha_emision=venta['fecha_emision'],
                    cliente=venta['cliente'],
                    rut_cliente=venta['rut_cliente'],
                    monto_exento=venta['monto_exento'],
                    monto_neto=venta['monto_neto'],
                    monto_iva=venta['monto_iva'],
                    monto_total=venta['monto_total'],
                    pagada=False,
                    origen_libro=fecha_libro
                )
                creadas += 1

        print(f"Ventas actualizadas: {actualizadas}, creadas: {creadas}")
        return redirect('listar_ventas')

    return render(request, 'crear_venta.html')

from django.utils import timezone
from django.db.models import Sum


def listar_ventas(request):
    ventas = FacturaVenta.objects.all().order_by('-fecha_emision')

    # Filtros
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    rut = request.GET.get('rut')
    folio = request.GET.get('folio')
    estado = request.GET.get('estado')

    if fecha_inicio and fecha_fin:
        try:
            inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            ventas = ventas.filter(fecha_emision__range=(inicio_dt, fin_dt))
        except ValueError:
            pass

    if rut:
        ventas = ventas.filter(rut_cliente__icontains=rut)

    if folio:
        ventas = ventas.filter(folio__icontains=folio)

    if estado == 'pendiente':
        ventas = ventas.filter(pagada=False)
    elif estado == 'pagada':
        ventas = ventas.filter(pagada=True)

    # Procesar cambios
    if request.method == 'POST':
        seleccionadas = request.POST.getlist('venta_id')
        folio_desbloqueo = request.POST.get('folio_desbloqueo', '').strip()
        clave_desbloqueo = request.POST.get('clave_desbloqueo', '').strip()
        clave_correcta = "DESBLOQUEAR2025"

        for venta in ventas:
            # ✅ Guardar comprobante si se subió
            file_field = f'comprobante_{venta.id}'
            if file_field in request.FILES:
                venta.comprobante = request.FILES[file_field]

            # ✅ Marcar como pagada o desbloquear
            if venta.pagada:
                if str(venta.id) not in seleccionadas and venta.folio == folio_desbloqueo and clave_desbloqueo == clave_correcta:
                    venta.pagada = False
                    venta.fecha_pago = None
            else:
                if str(venta.id) in seleccionadas:
                    venta.pagada = True
                    venta.fecha_pago = timezone.now().date()

            venta.save()

        return redirect(request.get_full_path())
    total_filtrado = ventas.aggregate(total=Sum('monto_total'))['total'] or 0


    return render(request, 'listar_ventas.html', {
        'ventas': ventas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'rut': rut,
        'folio': folio,
        'estado': estado,
        'total_filtrado': total_filtrado,
    })
# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import FacturaVenta
from django.utils import timezone

def cobrar_venta(request, venta_id):
    venta = get_object_or_404(FacturaVenta, id=venta_id)
    venta.pagada = True
    venta.fecha_pago = timezone.now().date()
    venta.save()
    return redirect('listar_ventas')

from django.shortcuts import render
from .models import FacturaVenta
from .utils import leer_ventas_desde_archivo  # función que tú defines

def actualizar_montos_ventas(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        actualizadas = 0
        no_encontradas = []

        for factura in leer_ventas_desde_archivo(archivo):
            folio = factura['folio']
            try:
                obj = FacturaVenta.objects.get(folio=folio)
                obj.monto_total = factura['monto_total']
                obj.save()
                actualizadas += 1
            except FacturaVenta.DoesNotExist:
                no_encontradas.append(folio)

        context = {
            'actualizadas': actualizadas,
            'no_encontradas': no_encontradas,
        }
        return render(request, 'resultado_actualizacion_ventas.html', context)

    return render(request, 'subir_actualizacion_ventas.html')