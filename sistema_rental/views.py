from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

# views.py
from django.shortcuts import render, redirect
from .models import Cliente

def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')

        Cliente.objects.create(
            nombre=nombre,
            rut=rut,
            direccion=direccion,
            telefono=telefono,
            correo=correo
        )
        return redirect('menu_rental')  # Asegúrate de tener esta URL definida

    return render(request, 'creacion_cliente.html')  # Usa el nombre correcto del template

# views.py
from django.shortcuts import render, redirect
from .models import Producto

def crear_producto(request):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        codigo = request.POST.get('codigo')
        precio = request.POST.get('precio_costo_unitario')
        fecha_compra = request.POST.get('fecha_compra')
        ultima_compra = request.POST.get('ultima_compra') or None
        proveedor = request.POST.get('proveedor')

        Producto.objects.create(
            descripcion=descripcion,
            codigo=codigo,
            precio_costo_unitario=precio,
            fecha_compra=fecha_compra,
            ultima_compra=ultima_compra,
            proveedor=proveedor
        )
        return redirect('menu_rental')  # Asegúrate de tener esta URL definida

    return render(request, 'creacion_producto.html')


# views.py
from django.shortcuts import render
from .models import Cliente
from django.db.models import Q

def listar_clientes(request):
    query = request.GET.get('q', '')
    if query:
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) | Q(rut__icontains=query)
        )
    else:
        clientes = Cliente.objects.all()

    return render(request, 'base_datos.html', {
        'clientes': clientes
    })

# views.py
from django.shortcuts import render
from .models import Producto
from django.db.models import Q

def listar_productos(request):
    query = request.GET.get('buscar', '')
    if query:
        productos = Producto.objects.filter(
            Q(descripcion__icontains=query) | Q(codigo__icontains=query)
        )
    else:
        productos = Producto.objects.all()

    return render(request, 'base_productos.html', {
        'productos': productos
    })

from django.shortcuts import render, redirect
from .models import Producto

def consulta_codigo(request):
    productos = Producto.objects.all().order_by('descripcion')

    if request.method == 'POST':
        # Si decides usar el formulario para enviar datos, puedes capturarlos aquí
        producto_id = request.POST.get('product_id')
        codigo = request.POST.get('codigo')
        precio = request.POST.get('precio_unitario')
        fecha = request.POST.get('fecha')
        otro = request.POST.get('otro')

        # Aquí podrías guardar, redirigir o mostrar un mensaje
        # return redirect('alguna_vista')

    return render(request, 'consulta_codigo.html', {
        'products': productos
    })

from .models import Producto, ProductoNuevo

def cotizaciones(request):
    productos = Producto.objects.all().order_by('descripcion')
    productos_nuevos = ProductoNuevo.objects.all().order_by('descripcion')
    return render(request, 'cotizaciones.html', {
        'productos': productos,
        'productos_nuevos': productos_nuevos
    })

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Producto, ProductoNuevo

@require_GET
def buscar_productos(request):
    q = request.GET.get('q', '').strip().lower()

    productos_existentes = Producto.objects.filter(descripcion__icontains=q)
    productos_nuevos = ProductoNuevo.objects.filter(descripcion__icontains=q)

    resultados = list(productos_existentes[:10]) + list(productos_nuevos[:10])  # máximo 10 en total

    data = [
        {
            'codigo': p.codigo,
            'descripcion': p.descripcion,
            'precio': p.precio_costo_unitario,
            'tipo': 'existente' if isinstance(p, Producto) else 'nuevo'
        }
        for p in resultados
    ]
    return JsonResponse(data, safe=False)

from django.shortcuts import render, redirect


from .models import Compra2, ProductoCompra

def ingreso_compra(request):
    if request.method == 'POST':
        compra = Compra2.objects.create(
            fecha=request.POST.get('fecha'),
            factura=request.POST.get('factura'),
            proveedor=request.POST.get('proveedor')
        )

        index = 0
        while True:
            descripcion = request.POST.get(f'descripcion_{index}')
            if not descripcion:
                break
            ProductoCompra.objects.create(
                compra=compra,
                descripcion=descripcion,
                codigo=request.POST.get(f'codigo_{index}'),
                cantidad=int(request.POST.get(f'cantidad_{index}')),
                precio_unitario=float(request.POST.get(f'p_unitario_{index}')),
                iva_porcentaje=float(request.POST.get(f'iva_porcentaje_{index}')),
                neto=float(request.POST.get(f'neto_{index}')),
                impuesto=float(request.POST.get(f'impuesto_{index}')),
                total=float(request.POST.get(f'total_{index}'))
            )
            index += 1

        return redirect('menu_rental')
    return render(request, 'ingreso_compra.html')

from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import CompraCamiones, VentaCamiones, PagoCamiones

from django.db.models import Sum
from .models import CompraCamiones

def gardilcic(request):
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        if tipo == 'compra':
            CompraCamiones.objects.create(
                mes=request.POST.get('mes'),
                fecha=request.POST.get('fecha'),
                factura=request.POST.get('factura'),
                total=request.POST.get('total'),
                mensaje=request.POST.get('mensaje'),
                pagado=request.POST.get('pagado') or 0,
                fecha_pago=request.POST.get('fecha_pago') or None,
                estado=request.POST.get('estado')
            )
        elif tipo == 'editar_compra':
            compra = CompraCamiones.objects.get(id=request.POST.get('compra_id'))
            compra.pagado = request.POST.get('pagado') or 0
            compra.fecha_pago = request.POST.get('fecha_pago') or None
            compra.estado = request.POST.get('estado')
            compra.save()
        return redirect('gardilcic')

    compras = CompraCamiones.objects.all().order_by('mes')

    ventas_por_mes = CompraCamiones.objects.values('mes').annotate(total=Sum('total')).order_by('mes')
    pagos_por_mes = CompraCamiones.objects.values('mes').annotate(total=Sum('pagado')).order_by('mes')

    # Emparejar pagos y ventas por mes
    resumen_por_mes = []
    ventas_dict = {v['mes']: v['total'] for v in ventas_por_mes}
    pagos_dict = {p['mes']: p['total'] for p in pagos_por_mes}

    for mes in ventas_dict:
        pagado = pagos_dict.get(mes, 0)
        deuda = ventas_dict[mes] - pagado
        resumen_por_mes.append({
            'mes': mes,
            'ventas': ventas_dict[mes],
            'pagado': pagado,
            'deuda': deuda
        })

    total_compras = compras.aggregate(total=Sum('total'))['total'] or 0
    total_pagado = compras.aggregate(total=Sum('pagado'))['total'] or 0
    total_deuda = total_compras - total_pagado

    return render(request, 'cta_cte_gardilcic.html', {
        'meses': meses,
        'compras': compras,
        'ventas': ventas_por_mes,
        'resumen_por_mes': resumen_por_mes,
        'total_compras': total_compras,
        'total_pagado': total_pagado,
        'total_deuda': total_deuda,
    })
from django.db.models import Sum

from django.shortcuts import render
from django.db.models import Q, Sum
from .models import ProductoCompra  # Asegúrate de importar correctamente

def consulta_compra(request):
    query = request.GET.get('q', '').strip()

    productos = ProductoCompra.objects.select_related('compra').all()

    if query:
        productos = productos.filter(
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )

    total_compras = productos.aggregate(total=Sum('total'))['total'] or 0

    return render(request, 'consulta_compra.html', {
        'productos': productos,
        'total_compras': total_compras,
        'query': query,
    })

from datetime import datetime, date
from django.shortcuts import render, redirect
from .models import Producto, Cotizacion, OrdenCompra, DetalleOrden, ProductoNuevo

def orden_compra(request):
    productos = Producto.objects.all()
    cotizaciones = Cotizacion.objects.select_related('cliente').order_by('-fecha')[:10]
    ultimo = OrdenCompra.objects.order_by('-numero').first()
    siguiente_numero = (ultimo.numero + 1) if ultimo else 1

    if request.method == 'POST':
        cliente = request.POST.get('cliente', '').strip()
        fecha_str = request.POST.get('fecha', '').strip()

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            fecha = date.today()

        try:
            neto = int(request.POST.get('neto', 0))
            iva = int(request.POST.get('iva', 0))
            total = int(request.POST.get('total', 0))
        except ValueError:
            neto, iva, total = 0, 0, 0

        orden = OrdenCompra.objects.create(
            numero=siguiente_numero,
            fecha=fecha,
            cliente=cliente,
            neto=neto,
            iva=iva,
            total=total
        )

        for i in range(0, 100):
            codigo = request.POST.get(f'codigo_{i}', '').strip()
            descripcion = request.POST.get(f'descripcion_{i}', '').strip()
            cantidad_raw = request.POST.get(f'cantidad_{i}', '').strip()
            precio_raw = request.POST.get(f'precio_{i}', '').strip()

            if codigo and cantidad_raw and precio_raw:
                try:
                    cantidad = float(cantidad_raw)
                    precio = float(precio_raw)

                    producto = Producto.objects.filter(codigo=codigo).first()

                    if producto:
                        DetalleOrden.objects.create(
                            orden=orden,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=precio,
                            total=cantidad * precio
                        )
                    elif descripcion:
                        producto_nuevo = ProductoNuevo.objects.create(
                            codigo=codigo,
                            descripcion=descripcion
                        )
                        DetalleOrden.objects.create(
                            orden=orden,
                            producto_nuevo=producto_nuevo,
                            cantidad=cantidad,
                            precio_unitario=precio,
                            total=cantidad * precio
                        )
                    else:
                        print(f"Producto con código {codigo} ignorado: sin descripción válida.")
                except Exception as e:
                    print(f"Error al guardar producto {codigo}: {e}")

        return redirect('listar_ordenes')

    return render(request, 'orden_compra.html', {
        'productos': productos,
        'cotizaciones': cotizaciones,
        'numero_siguiente': f"{siguiente_numero:05d}",
        'today': date.today()
    })

def listar_ordenes(request):
    ordenes = OrdenCompra.objects.prefetch_related('detalles').order_by('-fecha')
    return render(request, 'listar_ordenes.html', {'ordenes': ordenes})

def menu_facturas(request):
    return render(request, 'menu_facturas.html')

def menu_rental(request):
    return render(request, 'menu_rentalmix.html')


    
from django.shortcuts import render
from .models import Cliente, Producto, Cotizacion, DetalleCotizacion

def menu_informes(request):
    context = {
        'clientes': Cliente.objects.all().order_by('nombre'),
        'productos': Producto.objects.all().order_by('descripcion'),
        'cotizaciones': Cotizacion.objects.all().order_by('-fecha'),
        'detalles': DetalleCotizacion.objects.select_related('cotizacion').order_by('-cotizacion__fecha')
    }
    return render(request, 'menu_informes.html', context)

def editar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.rut = request.POST.get('rut')
        cliente.direccion = request.POST.get('direccion')
        cliente.telefono = request.POST.get('telefono')
        cliente.correo = request.POST.get('correo')
        cliente.save()
        return redirect('base_datos')  # Asegúrate de tener esta URL definida

    return render(request, 'editar_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('base_datos')  # Asegúrate de tener esta URL definida

    return render(request, 'eliminar_cliente.html', {'cliente': cliente})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.fecha_compra = request.POST.get('fecha_compra')
        producto.proveedor = request.POST.get('proveedor')
        producto.descripcion = request.POST.get('descripcion')
        producto.codigo = request.POST.get('codigo')  # si quieres permitir edición
        producto.factura = request.POST.get('factura')  # solo si agregaste el campo

        producto.cantidad = int(request.POST.get('cantidad') or 0)
        producto.precio_costo_unitario = float(request.POST.get('precio_costo_unitario') or 0)
        producto.iva_porcentaje = float(request.POST.get('iva_porcentaje') or 19)

        producto.neto = producto.cantidad * producto.precio_costo_unitario
        producto.impuesto = producto.neto * (producto.iva_porcentaje / 100)
        producto.total = producto.neto + producto.impuesto

        producto.save()
        return redirect('listar_productos')

    return render(request, 'editar_producto.html', {'producto': producto})


def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')  # Asegúrate de tener esta URL definida

    return render(request, 'eliminar_producto.html', {'producto': producto})

def costos_fijos_2024(request):
    return render(request, 'costos_fijos_2024.html')

def costos_fijos_2025(request):
    return render(request, 'costos_fijos_2025.html')

from django.shortcuts import render
from django.db.models import Sum, Q
from compras.models import FacturaCompra
from ventas.models import FacturaVenta
from otros.models import RegistroOtro
from sueldos.models import Sueldo
from obligaciones.models import PagoF29, PagoPreviRed  # ← asegúrate de tener estos modelos

def prueba_cst_fijos(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    filtros_emision = Q()
    filtros_otros = Q()
    filtros_sueldos = Q()
    filtros_obligaciones = Q()

    if fecha_inicio and fecha_fin:
        filtros_emision = Q(fecha_emision__range=[fecha_inicio, fecha_fin])
        filtros_otros = Q(fecha__range=[fecha_inicio, fecha_fin])
        filtros_sueldos = Q(fecha_pago__range=[fecha_inicio, fecha_fin])
        filtros_obligaciones = Q(fecha_pago__range=[fecha_inicio, fecha_fin])

    # Ventas pagadas
    ventas = FacturaVenta.objects.filter(pagada=True).filter(filtros_emision)
    total_ventas = ventas.aggregate(total=Sum('monto_total'))['total'] or 0

    # Compras pagadas
    compras = FacturaCompra.objects.filter(pagada=True).filter(filtros_emision)
    total_compras = compras.aggregate(total=Sum('monto_total'))['total'] or 0

    # Otros egresos
    otros = RegistroOtro.objects.filter(filtros_otros)
    total_boletas = otros.filter(tipo='boletas').aggregate(total=Sum('monto'))['total'] or 0
    total_partes = otros.filter(tipo='partes').aggregate(total=Sum('monto'))['total'] or 0
    total_patentes = otros.filter(tipo='patentes').aggregate(total=Sum('monto'))['total'] or 0
    total_otros_directos = otros.filter(tipo='otros').aggregate(total=Sum('monto'))['total'] or 0

    # Sueldos
    sueldos = Sueldo.objects.filter(filtros_sueldos)
    total_sueldos = sueldos.aggregate(total=Sum('monto'))['total'] or 0

    # Obligaciones: F29 y PreviRed
    total_f29 = PagoF29.objects.filter(filtros_obligaciones).aggregate(total=Sum('monto'))['total'] or 0
    total_previred = PagoPreviRed.objects.filter(filtros_obligaciones).aggregate(total=Sum('monto'))['total'] or 0
    total_obligaciones = total_f29 + total_previred

    # Total otros egresos
    total_otros = total_boletas + total_partes + total_patentes + total_otros_directos

    # Saldo final
    saldo = total_ventas - (total_compras + total_otros + total_sueldos + total_obligaciones)

    context = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total_ventas': total_ventas,
        'total_compras': total_compras,
        'total_boletas': total_boletas,
        'total_partes': total_partes,
        'total_patentes': total_patentes,
        'total_otros_directos': total_otros_directos,
        'total_otros': total_otros,
        'total_sueldos': total_sueldos,
        'total_f29': total_f29,
        'total_previred': total_previred,
        'total_obligaciones': total_obligaciones,
        'saldo': saldo,
    }

    return render(request, 'prueba.html', context)

import csv
from django.shortcuts import render, redirect
from .models import Producto

def importar_productos(request):
    preview = []
    mensaje = None

    if request.method == 'POST':
        confirmar = request.POST.get('confirmar')
        archivo = request.FILES.get('archivo')

        if archivo and archivo.name.endswith('.csv'):
            decoded = archivo.read().decode('latin-1').splitlines()
            reader = csv.DictReader(decoded)

            if confirmar == '1':
                # Confirmar e importar
                contador = 0
                for fila in reader:
                    try:
                        precio = float(fila['Precio Unitario'].replace('$', '').replace('.', '').replace(',', '.'))
                    except:
                        precio = 0

                    fecha_compra = fila.get('Fecha de Compra')
                    try:
                        fecha_compra = datetime.strptime(fecha_compra, '%d/%m/%Y').date() if fecha_compra else None
                    except:
                        fecha_compra = None

                    Producto.objects.update_or_create(
                        codigo=fila['CODIGO'],
                        defaults={
                            'descripcion': fila['DESCRIPCION'],
                            'precio_costo_unitario': precio,
                            'fecha_compra': fecha_compra,
                            'proveedor': fila.get('Proveedor', '')
                        }
                    )
                    contador += 1
                mensaje = f"✅ Se importaron {contador} productos correctamente."
            else:
                # Vista previa
                for fila in reader:
                    preview.append({
                        'descripcion': fila['DESCRIPCION'],
                        'codigo': fila['CODIGO'],
                        'precio': fila['Precio Unitario'],
                        'fecha': fila.get('Fecha de Compra'),
                        'proveedor': fila.get('Proveedor', '')
                    })

            return render(request, 'importar_productos.html', {
                'preview': preview,
                'mensaje': mensaje
            })

        else:
            mensaje = "❌ El archivo debe ser CSV."

    return render(request, 'importar_productos.html', {'mensaje': mensaje})

import csv
from datetime import datetime
from django.shortcuts import render, redirect
from .models import Producto

def importar_productos(request):
    preview = []
    mensaje = None

    if request.method == 'POST':
        confirmar = request.POST.get('confirmar')

        if confirmar == '1':
            # Confirmar importación desde sesión
            contenido = request.session.get('csv_preview')
            if not contenido:
                mensaje = "❌ No se encontró el archivo para importar."
                return render(request, 'importar_productos.html', {'mensaje': mensaje})

            reader = csv.DictReader(contenido.splitlines())
            contador = 0
            for fila in reader:
                try:
                    precio = float(fila['Precio Unitario'].replace('$', '').replace('.', '').replace(',', '.'))
                except:
                    precio = 0

                try:
                    fecha = datetime.strptime(fila.get('Fecha de Compra', ''), '%d/%m/%Y').date()
                except:
                    fecha = None

                Producto.objects.update_or_create(
                    codigo=fila['CODIGO'],
                    defaults={
                        'descripcion': fila['DESCRIPCION'],
                        'precio_costo_unitario': precio,
                        'fecha_compra': fecha,
                        'proveedor': fila.get('Proveedor', '')
                    }
                )
                contador += 1

            request.session.pop('csv_preview', None)
            mensaje = f"✅ Se importaron {contador} productos correctamente."
            return render(request, 'importar_productos.html', {'mensaje': mensaje})

        else:
            archivo = request.FILES.get('archivo')
            if archivo and archivo.name.endswith('.csv'):
                contenido = archivo.read().decode('latin-1')
                request.session['csv_preview'] = contenido
                reader = csv.DictReader(contenido.splitlines())
                for fila in reader:
                    preview.append({
                        'descripcion': fila['DESCRIPCION'],
                        'codigo': fila['CODIGO'],
                        'precio': fila['Precio Unitario'],
                        'fecha': fila.get('Fecha de Compra'),
                        'proveedor': fila.get('Proveedor', '')
                    })
                return render(request, 'importar_productos.html', {'preview': preview})
            else:
                mensaje = "❌ El archivo debe ser CSV."

    return render(request, 'importar_productos.html', {'mensaje': mensaje})

import csv
import unicodedata
from django.shortcuts import render
from .models import Cliente

def limpiar(texto):
    """Normaliza texto eliminando tildes, espacios y mayúsculas."""
    if not texto:
        return ''
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').strip().lower()

def importar_clientes(request):
    preview = []
    mensaje = None

    if request.method == 'POST':
        confirmar = request.POST.get('confirmar')
        archivo = request.FILES.get('archivo')

        if confirmar == '1':
            # Confirmar importación desde sesión
            contenido = request.session.get('csv_clientes')
            if not contenido:
                mensaje = "❌ No se encontró el archivo para importar."
                return render(request, 'importar_clientes.html', {'mensaje': mensaje})

            reader = csv.DictReader(contenido.splitlines())
            campos = {limpiar(c): c for c in reader.fieldnames}

            contador = 0
            for fila in reader:
                Cliente.objects.update_or_create(
                    rut=fila.get(campos.get('rut'), ''),
                    defaults={
                        'nombre': fila.get(campos.get('cliente'), ''),
                        'direccion': fila.get(campos.get('direccion'), ''),
                        'telefono': fila.get(campos.get('celular'), ''),
                        'correo': fila.get(campos.get('e_mail'), '')
                    }
                )
                contador += 1

            request.session.pop('csv_clientes', None)
            mensaje = f"✅ Se importaron {contador} clientes correctamente."
            return render(request, 'importar_clientes.html', {'mensaje': mensaje})

        elif archivo and archivo.name.endswith('.csv'):
            # Vista previa
            contenido = archivo.read().decode('latin-1')
            request.session['csv_clientes'] = contenido
            reader = csv.DictReader(contenido.splitlines())
            campos = {limpiar(c): c for c in reader.fieldnames}

            for fila in reader:
                preview.append({
                    'nombre': fila.get(campos.get('cliente'), ''),
                    'rut': fila.get(campos.get('rut'), ''),
                    'direccion': fila.get(campos.get('direccion'), ''),
                    'telefono': fila.get(campos.get('celular'), ''),
                    'correo': fila.get(campos.get('e_mail'), '')
                })

            return render(request, 'importar_clientes.html', {'preview': preview})
        else:
            mensaje = "❌ El archivo debe ser CSV."

    return render(request, 'importar_clientes.html', {'mensaje': mensaje})

from django.shortcuts import get_object_or_404, redirect
from .models import OrdenCompra, NumeroOrdenDisponible

def eliminar_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)

    # Guardar el número como disponible
    NumeroOrdenDisponible.objects.get_or_create(numero=orden.numero)

    # Eliminar la orden
    orden.delete()

    return redirect('listar_ordenes')  # Ajusta según tu URL

from django.shortcuts import get_object_or_404, redirect
from .models import ProductoCompra

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(ProductoCompra, id=producto_id)
    producto.delete()
    return redirect('consulta_compra')

from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductoCompra

def editar_compra(request, producto_id):
    producto = get_object_or_404(ProductoCompra, id=producto_id)

    if request.method == 'POST':
        producto.descripcion = request.POST.get('descripcion')
        producto.codigo = request.POST.get('codigo')
        producto.cantidad = int(request.POST.get('cantidad'))
        producto.precio_unitario = float(request.POST.get('precio_unitario'))
        producto.iva_porcentaje = float(request.POST.get('iva_porcentaje'))

        producto.neto = producto.cantidad * producto.precio_unitario
        producto.impuesto = producto.neto * (producto.iva_porcentaje / 100)
        producto.total = producto.neto + producto.impuesto

        producto.save()
        return redirect('consulta_compra')

    return render(request, 'editar_compra.html', {'producto': producto})

from django.db.models import Q, Sum
from django.shortcuts import render
from ventas.models import FacturaVenta
from compras.models import FacturaCompra
from otros.models import RegistroOtro
from sueldos.models import Sueldo
from obligaciones.models import PagoF29, PagoPreviRed  # ← nuevos modelos

def costos_fijos_detallados(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Filtros por fecha_emision
    filtros_emision = Q()
    if fecha_inicio and fecha_fin:
        filtros_emision = Q(fecha_emision__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        filtros_emision = Q(fecha_emision__gte=fecha_inicio)
    elif fecha_fin:
        filtros_emision = Q(fecha_emision__lte=fecha_fin)

    # Filtros por fecha (otros egresos)
    filtros_otros = Q()
    if fecha_inicio and fecha_fin:
        filtros_otros = Q(fecha__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        filtros_otros = Q(fecha__gte=fecha_inicio)
    elif fecha_fin:
        filtros_otros = Q(fecha__lte=fecha_fin)

    # Filtros por fecha_pago (sueldos y obligaciones)
    filtros_sueldos = filtros_obligaciones = Q()
    if fecha_inicio and fecha_fin:
        filtros_sueldos = Q(fecha_pago__range=[fecha_inicio, fecha_fin])
        filtros_obligaciones = Q(fecha_pago__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        filtros_sueldos = Q(fecha_pago__gte=fecha_inicio)
        filtros_obligaciones = Q(fecha_pago__gte=fecha_inicio)
    elif fecha_fin:
        filtros_sueldos = Q(fecha_pago__lte=fecha_fin)
        filtros_obligaciones = Q(fecha_pago__lte=fecha_fin)

    # Inicializar variables
    ventas = compras = otros_detallados = sueldos = pagos_f29 = pagos_previred = []
    total_ventas = total_compras = total_boletas = total_partes = total_patentes = otros = total_otros = total_sueldos = total_f29 = total_previred = total_obligaciones = saldo = None

    if fecha_inicio and fecha_fin:
        # Ventas
        ventas = FacturaVenta.objects.filter(pagada=True).filter(filtros_emision)
        total_ventas = ventas.aggregate(total=Sum('monto_total'))['total'] or 0

        # Compras
        compras = FacturaCompra.objects.filter(pagada=True).filter(filtros_emision)
        total_compras = compras.aggregate(total=Sum('monto_total'))['total'] or 0

        # Otros egresos
        otros_detallados = RegistroOtro.objects.filter(filtros_otros)
        total_boletas = otros_detallados.filter(tipo='boletas').aggregate(total=Sum('monto'))['total'] or 0
        total_partes = otros_detallados.filter(tipo='partes').aggregate(total=Sum('monto'))['total'] or 0
        total_patentes = otros_detallados.filter(tipo='patentes').aggregate(total=Sum('monto'))['total'] or 0
        otros = otros_detallados.filter(tipo='otros').aggregate(total=Sum('monto'))['total'] or 0
        total_otros = total_boletas + total_partes + total_patentes + otros

        # Sueldos
        sueldos = Sueldo.objects.filter(filtros_sueldos)
        total_sueldos = sueldos.aggregate(total=Sum('monto'))['total'] or 0

        # Obligaciones
        pagos_f29 = PagoF29.objects.filter(filtros_obligaciones)
        pagos_previred = PagoPreviRed.objects.filter(filtros_obligaciones)
        total_f29 = pagos_f29.aggregate(total=Sum('monto'))['total'] or 0
        total_previred = pagos_previred.aggregate(total=Sum('monto'))['total'] or 0
        total_obligaciones = total_f29 + total_previred

        # Saldo final
        saldo = total_ventas - (total_compras + total_otros + total_sueldos + total_obligaciones)

    context = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'ventas': ventas,
        'compras': compras,
        'otros_detallados': otros_detallados,
        'sueldos': sueldos,
        'pagos_f29': pagos_f29,
        'pagos_previred': pagos_previred,
        'total_ventas': total_ventas,
        'total_compras': total_compras,
        'total_boletas': total_boletas,
        'total_partes': total_partes,
        'total_patentes': total_patentes,
        'otros': otros,
        'total_otros': total_otros,
        'total_sueldos': total_sueldos,
        'total_f29': total_f29,
        'total_previred': total_previred,
        'total_obligaciones': total_obligaciones,
        'saldo': saldo,
    }

    return render(request, 'costos_fijos_detallados.html', context)

from django.shortcuts import render
from .models import Cotizacion

def listado_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all().order_by('-fecha')
    return render(request, 'listado_cotizaciones.html', {'cotizaciones': cotizaciones})

def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id=orden_id)
    detalles = orden.detalles.all()
    return render(request, 'detalle_orden.html', {
        'orden': orden,
        'detalles': detalles
    })
    
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Cotizacion, DetalleCotizacion
import json

@csrf_exempt
def guardar_cotizacion(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Crear cotización con los nombres correctos
        cotizacion = Cotizacion.objects.create(
            observaciones=data.get('observaciones', ''),
            total_neto=data.get('neto', 0),
            total_iva=data.get('iva', 0),
            total_final=data.get('total', 0)
        )

        # Crear detalles
        for item in data.get('productos', []):
            DetalleCotizacion.objects.create(
                cotizacion=cotizacion,
                producto=item['producto'],
                codigo=item['codigo'],
                precio_unitario=item['precio'],
                cantidad=item['cantidad'],
                subtotal=item['subtotal'],
                iva=item['iva'],
                total=item['total']
            )

        return JsonResponse({'success': True, 'id': cotizacion.id})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import ProductoCompra, Producto  # Asegurate que los modelos estén bien nombrados

def salida_producto(request):
    productos_nuevos = ProductoCompra.objects.all()
    productos_inventario = Producto.objects.all()

    # Asignamos origen a cada producto
    for p in productos_nuevos:
        p.origen = 'compra'
    for p in productos_inventario:
        p.origen = 'inventario'

    productos = list(productos_nuevos) + list(productos_inventario)

    return render(request, 'salida_producto.html', {'productos': productos})


@require_POST
def disminuir_producto(request, id):
    origen = request.POST.get('origen')

    if origen == 'compra':
        producto = get_object_or_404(ProductoCompra, id=id)
    else:
        producto = get_object_or_404(Producto, id=id)

    if producto.cantidad > 0:
        producto.cantidad -= 1
        producto.save()

    return redirect('salida_producto')

    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ProductoNuevo
from decimal import Decimal
from datetime import datetime

def crear_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio_costo_unitario = request.POST.get('precio_costo_unitario', '0').strip()
        cantidad = request.POST.get('cantidad', '1').strip()
        fecha_compra = request.POST.get('fecha_compra', '').strip()
        ultima_compra = request.POST.get('ultima_compra', '').strip()
        proveedor = request.POST.get('proveedor', '').strip()

        if not codigo or not descripcion or not precio_costo_unitario:
            messages.error(request, "Debes completar los campos obligatorios.")
            return redirect('crear_producto')

        if ProductoNuevo.objects.filter(codigo=codigo).exists():
            messages.error(request, "Ya existe un producto con ese código.")
            return redirect('crear_producto')

        try:
            producto = ProductoNuevo.objects.create(
                codigo=codigo,
                descripcion=descripcion,
                precio_costo_unitario=Decimal(precio_costo_unitario),
                cantidad=Decimal(cantidad),
                fecha_compra=datetime.strptime(fecha_compra, '%Y-%m-%d') if fecha_compra else None,
                ultima_compra=datetime.strptime(ultima_compra, '%Y-%m-%d') if ultima_compra else None,
                proveedor=proveedor
            )
            messages.success(request, f"Producto '{producto.descripcion}' creado correctamente.")
            return redirect('cotizaciones')  # Ajusta según tu flujo
        except Exception as e:
            messages.error(request, f"Error al crear el producto: {e}")
            return redirect('crear_producto')

    return render(request, 'creacion_producto.html')

from django.http import JsonResponse
from .models import DetalleCotizacion

def cotizacion_detalles_json(request, cotizacion_id):
    detalles = DetalleCotizacion.objects.filter(cotizacion_id=cotizacion_id)
    data = {
        'detalles': [
            {
                'codigo': d.codigo,
                'producto': d.producto,
                'cantidad': d.cantidad,
                'precio': d.precio_unitario
            } for d in detalles
        ]
    }
    return JsonResponse(data)


from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

@user_passes_test(lambda u: u.is_superuser)
def crear_usuario(request):
    grupos = Group.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        modulos = request.POST.getlist('modulos')

        user = User.objects.create_user(username=username, email=email, password=password)
        for nombre_grupo in modulos:
            grupo = Group.objects.get(name=nombre_grupo)
            user.groups.add(grupo)

        return redirect('menu_principal')

    return render(request, 'crear_usuario.html', {'grupos': grupos})

def menu_rental(request):
    user = request.user
    context = {
        'acceso_clientes': user.groups.filter(name='clientes').exists() or user.is_superuser,
        'acceso_cotizacion': user.groups.filter(name='cotizacion').exists() or user.is_superuser,
        'acceso_inventario': user.groups.filter(name='inventario').exists() or user.is_superuser,
        'acceso_reportes': user.groups.filter(name='reportes').exists() or user.is_superuser,
    }
    return render(request, 'menu_rentalmix.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def menu_facturas(request):
    user = request.user
    context = {
        'ver_compras': user.is_superuser or user.groups.filter(name='compras').exists(),
        'ver_ventas': user.is_superuser or user.groups.filter(name='ventas').exists(),
        'ver_sueldos': user.is_superuser or user.groups.filter(name='sueldos').exists(),
        'ver_f29': user.is_superuser or user.groups.filter(name='f29').exists(),
        'ver_previred': user.is_superuser or user.groups.filter(name='previred').exists(),
        'ver_otros': user.is_superuser or user.groups.filter(name='otros').exists(),
    }
    return render(request, 'menu_facturas.html', context)

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render

@user_passes_test(lambda u: u.is_superuser)
def ver_usuarios(request):
    usuarios = User.objects.all().order_by('username')
    return render(request, 'ver_usuarios.html', {'usuarios': usuarios})

from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    grupos = Group.objects.all()

    if request.method == 'POST':
        nuevos_grupos = request.POST.getlist('modulos')
        nuevo_email = request.POST.get('email', '').strip()

        # Actualizar correo
        usuario.email = nuevo_email
        usuario.save()

        # Actualizar grupos
        usuario.groups.clear()
        for nombre in nuevos_grupos:
            grupo = Group.objects.get(name=nombre)
            usuario.groups.add(grupo)

        return redirect('ver_usuarios')

    return render(request, 'editar_usuario.html', {'usuario': usuario, 'grupos': grupos})

@user_passes_test(lambda u: u.is_superuser)
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    return redirect('ver_usuarios')


from django.shortcuts import render, get_object_or_404
from .models import Cotizacion

def detalles_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    return render(request, 'detalles_cotizacion.html', {'cotizacion': cotizacion})

def eliminar_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    cotizacion.delete()
    return redirect('listado_cotizaciones')