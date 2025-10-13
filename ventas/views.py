from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Venta

def registrar_venta(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        cliente = request.POST.get('cliente')
        total = request.POST.get('total')
        pagado = request.POST.get('pagado') == 'on'
        documento = request.FILES.get('documento')

        venta = Venta(
            fecha=fecha,
            cliente=cliente,
            total=total,
            pagado=pagado,
            documento=documento
        )
        venta.save()

        mensaje = f"Venta registrada para {cliente} el {fecha} por ${total}. Estado: {'Pagado' if pagado else 'Pendiente'}."
        return render(request, 'crear_venta.html', {'mensaje': mensaje})

    return render(request, 'crear_venta.html')

from django.shortcuts import render
from .models import Venta

def listar_ventas(request):
    ventas = Venta.objects.order_by('-fecha')
    return render(request, 'listar_ventas.html', {'ventas': ventas})