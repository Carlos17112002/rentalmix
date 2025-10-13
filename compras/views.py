from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib import messages


import csv
import io
from django.shortcuts import render, redirect
from .models import LibroCompra

from django.shortcuts import render, redirect
from .models import LibroCompra

def subir_libro_compras(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        fecha = request.POST.get('fecha')
        total = request.POST.get('total')
        pagado = request.POST.get('pagado') == 'on'

        libro = LibroCompra(
            fecha=fecha,
            total=total,
            pagado=pagado,
            archivo=archivo,
            nombre_archivo=archivo.name,
            estado='procesando'
        )
        libro.save()

        return redirect('listar_compras')

    return render(request, 'subir_libro.html')
from django.shortcuts import render, get_object_or_404, redirect
from .models import LibroCompra

def listar_compras(request):
    compras = LibroCompra.objects.order_by('-fecha')
    return render(request, 'listar_compras.html', {'compras': compras})

import csv
import io

def revisar_libro(request, libro_id):
    libro = get_object_or_404(LibroCompra, id=libro_id)
    encabezados = []
    contenido = []

    if libro.archivo.name.endswith('.csv'):
        with open(libro.archivo.path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';', skipinitialspace=True)
            filas = list(reader)
            if filas:
                encabezados = filas[0]
                contenido = filas[1:]

    if request.method == 'POST':
        nuevo_csv = [encabezados]  # mantener encabezados
        for i in range(len(contenido)):
            fila = []
            for j in range(len(encabezados)):
                key = f'celda_{i}_{j}'
                valor = request.POST.get(key, '')
                fila.append(valor)
            nuevo_csv.append(fila)

        with open(libro.archivo.path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(nuevo_csv)

        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['correcto', 'error']:
            libro.estado = nuevo_estado
        libro.save()
        return redirect('listar_compras')

    return render(request, 'revisar_libro.html', {
        'libro': libro,
        'encabezados': encabezados,
        'contenido': contenido
    })

def eliminar_libro(request, libro_id):
    libro = get_object_or_404(LibroCompra, id=libro_id)
    libro.delete()
    return redirect('listar_compras')

from django.shortcuts import get_object_or_404, redirect
from .models import LibroCompra

from django.shortcuts import render, get_object_or_404, redirect
from .models import LibroCompra

def seleccionar_banco(request, libro_id):
    libro = get_object_or_404(LibroCompra, id=libro_id)

    if libro.estado != 'correcto':
        return redirect('listar_compras')  # solo se puede pagar si está correcto

    if request.method == 'POST':
        banco = request.POST.get('banco')
        if banco in ['banco_chile', 'scotiabank']:
            libro.pagado = True
            libro.save()
            # Aquí podrías guardar el banco seleccionado si lo agregas al modelo
            return redirect('listar_compras')

    return render(request, 'pagar_banco.html', {'libro': libro})