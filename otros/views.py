from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import RegistroOtro

def registrar_otro(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        monto = request.POST.get('monto') or None
        documento = request.FILES.get('documento')

        registro = RegistroOtro(
            tipo=tipo,
            descripcion=descripcion,
            fecha=fecha,
            monto=monto,
            documento=documento
        )
        registro.save()

        mensaje = f"{registro.get_tipo_display()} registrado correctamente."
        return render(request, 'crear_otros.html', {'mensaje': mensaje})

    return render(request, 'crear_otros.html')

from django.shortcuts import render
from .models import RegistroOtro

def listar_otros(request):
    otros = RegistroOtro.objects.order_by('-fecha')
    return render(request, 'listar_otros.html', {'otros': otros})