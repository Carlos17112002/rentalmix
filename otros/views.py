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
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    otros = RegistroOtro.objects.all()

    if desde and hasta:
        otros = otros.filter(fecha__range=[desde, hasta])

    return render(request, 'listar_otros.html', {
        'otros': otros
    })

from django.shortcuts import render, get_object_or_404, redirect
def eliminar_otro(request, id):
    registro = get_object_or_404(RegistroOtro, id=id)
    registro.delete()
    return redirect('listar_otros')

def editar_otro(request, id):
    registro = get_object_or_404(RegistroOtro, id=id)
    if request.method == 'POST':
        registro.tipo = request.POST.get('tipo')
        registro.descripcion = request.POST.get('descripcion')
        registro.fecha = request.POST.get('fecha')
        registro.monto = request.POST.get('monto')
        if request.FILES.get('documento'):
            registro.documento = request.FILES.get('documento')
        registro.save()
        return redirect('listar_otros')
    return render(request, 'editar_otro.html', {'registro': registro})