from django.shortcuts import render, redirect

# Create your views here.

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

def cotizaciones(request):
    productos = Producto.objects.all().order_by('descripcion')  # ordenados alfabéticamente
    return render(request, 'cotizaciones.html', {'productos': productos})


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

def gardilcic(request):
    meses = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

    if request.method == 'POST':
        tipo = request.POST.get('tipo')  # Para saber de qué formulario viene

        if tipo == 'compra':
            CompraCamiones.objects.create(
                mes=request.POST.get('mes'),
                fecha=request.POST.get('fecha'),
                factura=request.POST.get('factura'),
                total=request.POST.get('total'),
                mensaje=request.POST.get('mensaje'),
                pagado=True if request.POST.get('pagado') == 'Sí' else False,
                fecha_pago=request.POST.get('fecha_pago') or None,
                estado=request.POST.get('estado')
            )

        elif tipo == 'venta':
            VentaCamiones.objects.create(
                mes=request.POST.get('mes'),
                total=request.POST.get('total')
            )

        elif tipo == 'pago':
            PagoCamiones.objects.create(
                mes=request.POST.get('mes'),
                total=request.POST.get('total')
            )

        return redirect('gardilcic')  # Redirige para evitar reenvío del formulario

    # Datos para mostrar en las tablas
    compras = CompraCamiones.objects.all()
    ventas = VentaCamiones.objects.all()
    pagos = PagoCamiones.objects.all()

    return render(request, 'cta_cte_gardilcic.html', {
        'meses': meses,
        'compras': compras,
        'ventas': ventas,
        'pagos': pagos
    })

from django.db.models import Sum

def consulta_compra(request):
    productos = ProductoCompra.objects.select_related('compra').all()
    total_compras = productos.aggregate(total=Sum('total'))['total'] or 0
    return render(request, 'consulta_compra.html', {
        'productos': productos,
        'total_compras': total_compras
    })

def orden_compra(request):
    productos = Producto.objects.all()
    return render(request, 'orden_compra.html', {'productos': productos})


def menu_facturas(request):
    return render(request, 'menu_facturas.html')

def menu_rental(request):
    return render(request, 'menu_rentalmix.html')

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Cotizacion, DetalleCotizacion

@csrf_exempt
def guardar_cotizacion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cotizacion = Cotizacion.objects.create(
            observaciones=data.get('observaciones', ''),
            total_neto=data['total_neto'],
            total_iva=data['total_iva'],
            total_final=data['total_final']
        )
        for item in data['detalles']:
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
        return JsonResponse({'status': 'ok', 'id': cotizacion.id})
    
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

def editar_producto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == 'POST':
        producto.descripcion = request.POST.get('descripcion')
        producto.codigo = request.POST.get('codigo')
        producto.precio_costo_unitario = request.POST.get('precio_costo_unitario')
        producto.fecha_compra = request.POST.get('fecha_compra')
        producto.ultima_compra = request.POST.get('ultima_compra') or None
        producto.proveedor = request.POST.get('proveedor')
        producto.save()
        return redirect('listar_productos')  # Asegúrate de tener esta URL definida

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