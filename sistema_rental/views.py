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


def ingreso_compra(request):
    if request.method == 'POST':
        # Recoger datos del formulario de compra
        factura = request.POST.get('factura')
        proveedor = request.POST.get('proveedor')
        # ...procesar detalles de la compra e insertar en la base de datos...
        # Ejemplo: Purchase.objects.create(factura=factura, proveedor=proveedor, ...)
        success = "Compra registrada correctamente."
        return render(request, 'ingreso_compra.html', {'success': success})
    return render(request, 'ingreso_compra.html')

def gardilcic(request):
    if request.method == 'POST':
        # Recoger datos del formulario de cuenta corriente
        mes = request.POST.get('mes')
        total_pagado = request.POST.get('total')
        # ...realizar cálculos, actualizar estados de cuenta...
        # Ejemplo: update_payment(mes, total_pagado)
        success = "Operación en cuenta ejecutada correctamente."
        return render(request, 'cta_cte_gardilcic.html', {'success': success})
    return render(request, 'cta_cte_gardilcic.html')


def consulta_compra(request):
    return render(request, 'consulta_compra.html')

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
