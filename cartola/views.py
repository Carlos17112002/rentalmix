from django.shortcuts import render
from compras.models import FacturaCompra
from ventas.models import FacturaVenta
from sueldos.models import Sueldo
from obligaciones.models import PagoF29, PagoPreviRed
from cartola.models import SaldoInicialMensual
from datetime import date
from calendar import monthrange
from decimal import Decimal

def cartola_filtrada(request):
    hoy = date.today()
    mes = int(request.GET.get('mes', hoy.month))
    año = int(request.GET.get('año', hoy.year))

    fecha_inicio = date(año, mes, 1)
    fecha_fin = date(año, mes, monthrange(año, mes)[1])

    # Capturar o guardar saldo inicial si es enero
    saldo_inicial_obj = None
    if mes == 1:
        saldo_inicial_obj, _ = SaldoInicialMensual.objects.get_or_create(año=año, mes=mes)
        if request.method == "POST":
            try:
                nuevo_monto = Decimal(request.POST.get("saldo_inicial", "0").replace(",", "."))
                saldo_inicial_obj.monto = nuevo_monto
                saldo_inicial_obj.save()
            except:
                pass
        saldo_inicial = saldo_inicial_obj.monto
    else:
        # Obtener saldo inicial de enero
        saldo_enero = SaldoInicialMensual.objects.filter(año=año, mes=1).first()
        saldo_base = saldo_enero.monto if saldo_enero else Decimal("0")

        # Calcular movimientos acumulados desde enero hasta mes anterior
        fecha_inicio_acumulado = date(año, 1, 1)
        fecha_fin_acumulado = date(año, mes - 1, monthrange(año, mes - 1)[1])

        compras_previas = FacturaCompra.objects.filter(fecha_emision__range=(fecha_inicio_acumulado, fecha_fin_acumulado), pagada=True)
        ventas_previas = FacturaVenta.objects.filter(fecha_emision__range=(fecha_inicio_acumulado, fecha_fin_acumulado), pagada=True)
        sueldos_previos = Sueldo.objects.filter(fecha_pago__range=(fecha_inicio_acumulado, fecha_fin_acumulado), pagado=True)
        impuestos_previos = PagoF29.objects.filter(fecha_pago__range=(fecha_inicio_acumulado, fecha_fin_acumulado))
        cotizaciones_previos = PagoPreviRed.objects.filter(fecha_pago__range=(fecha_inicio_acumulado, fecha_fin_acumulado))

        saldo_inicial = saldo_base + sum([
            -compra.monto_total for compra in compras_previas
        ] + [
            venta.monto_total for venta in ventas_previas
        ] + [
            -sueldo.monto for sueldo in sueldos_previos
        ] + [
            -imp.monto for imp in impuestos_previos
        ] + [
            -cot.monto for cot in cotizaciones_previos
        ])

    # Transacciones del mes actual
    compras = FacturaCompra.objects.filter(fecha_emision__range=(fecha_inicio, fecha_fin), pagada=True)
    ventas = FacturaVenta.objects.filter(fecha_emision__range=(fecha_inicio, fecha_fin), pagada=True)
    sueldos = Sueldo.objects.filter(fecha_pago__range=(fecha_inicio, fecha_fin), pagado=True)
    impuestos = PagoF29.objects.filter(fecha_pago__range=(fecha_inicio, fecha_fin))
    cotizaciones = PagoPreviRed.objects.filter(fecha_pago__range=(fecha_inicio, fecha_fin))

    transacciones = []

    for compra in compras:
        transacciones.append({
            'fecha': compra.fecha_emision,
            'detalle': f"Compra a {compra.proveedor}",
            'documento': compra.folio,
            'cargo': compra.monto_total,
            'abono': Decimal("0"),
        })

    for venta in ventas:
        transacciones.append({
            'fecha': venta.fecha_emision,
            'detalle': f"Venta a {venta.cliente}",
            'documento': venta.folio,
            'cargo': Decimal("0"),
            'abono': venta.monto_total,
        })

    for sueldo in sueldos:
        transacciones.append({
            'fecha': sueldo.fecha_pago,
            'detalle': f"Sueldo pagado a {sueldo.trabajador}",
            'documento': "—",
            'cargo': sueldo.monto,
            'abono': Decimal("0"),
        })

    for imp in impuestos:
        transacciones.append({
            'fecha': imp.fecha_pago,
            'detalle': f"Pago de impuesto F29",
            'documento': "—",
            'cargo': imp.monto,
            'abono': Decimal("0"),
        })

    for cot in cotizaciones:
        transacciones.append({
            'fecha': cot.fecha_pago,
            'detalle': f"Pago de cotizaciones",
            'documento': "—",
            'cargo': cot.monto,
            'abono': Decimal("0"),
        })

    transacciones.sort(key=lambda x: x['fecha'])

    saldo = saldo_inicial
    for t in transacciones:
        saldo += t['abono'] - t['cargo']
        t['saldo'] = saldo

    context = {
        'transacciones': transacciones,
        'saldo_inicial': saldo_inicial,
        'saldo_final': saldo,
        'mes': mes,
        'año': año,
    }

    return render(request, 'cartola/cartola.html', context)