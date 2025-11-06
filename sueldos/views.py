from django.shortcuts import render, redirect, get_object_or_404
from .models import Sueldo

def listar_sueldos(request):
    sueldos = Sueldo.objects.order_by('-fecha_pago')
    return render(request, 'listar_sueldos.html', {'sueldos': sueldos})

from django.shortcuts import render, redirect
from .models import Sueldo, Trabajador

def agregar_sueldo(request):
    from .models import Sueldo, Trabajador

    trabajadores = Trabajador.objects.all()

    if request.method == 'POST':
        trabajador_id = request.POST.get('empleado')  # ← debe coincidir con name="empleado"
        documento = request.FILES.get('documento')
        monto = request.POST.get('monto')
        fecha_pago = request.POST.get('fecha_pago')

        if trabajador_id:  # ← evita el error si no se seleccionó nada
            Sueldo.objects.create(
                trabajador_id=trabajador_id,
                documento=documento,
                monto=monto,
                fecha_pago=fecha_pago
            )
            return redirect('listar_sueldos')

    return render(request, 'registrar_sueldo.html', {'trabajadores': trabajadores})

from django.shortcuts import render, get_object_or_404, redirect
from sueldos.models import Sueldo
from decimal import Decimal

def editar_sueldo(request, sueldo_id):
    sueldo = get_object_or_404(Sueldo, id=sueldo_id)

    if request.method == 'POST':
        if not sueldo.pagado:
            sueldo.empleado = request.POST.get('empleado', sueldo.empleado)
            monto_raw = request.POST.get('monto', '').replace(',', '.')
            try:
                sueldo.monto = Decimal(monto_raw)
            except:
                pass  # podrías agregar validación o mensaje de error aquí
            sueldo.fecha_pago = request.POST.get('fecha_pago', sueldo.fecha_pago)

        # Manejar documento siempre, esté pagado o no
        if 'documento' in request.FILES:
            sueldo.documento = request.FILES['documento']

        sueldo.save()
        return redirect('listar_sueldos')

    return render(request, 'editar_sueldo.html', {'sueldo': sueldo})

from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from .models import Sueldo

def pagar_sueldo(request, sueldo_id):
    sueldo = get_object_or_404(Sueldo, id=sueldo_id)
    if request.method == 'POST':
        sueldo.pagado = True
        sueldo.fecha_pago = date.today()  # ← actualiza con la fecha actual
        sueldo.save()
        return redirect('listar_sueldos')
    return render(request, 'pagar_sueldo.html', {'sueldo': sueldo})

def eliminar_sueldo(request, sueldo_id):
    sueldo = get_object_or_404(Sueldo, id=sueldo_id)
    sueldo.delete()
    return redirect('listar_sueldos')

# views.py
from django.shortcuts import render, redirect
from .models import Trabajador
from django import forms

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'rut', 'fecha_contrato']
        widgets = {
            'fecha_contrato': forms.DateInput(attrs={'type': 'date'}),
        }

def crear_trabajador(request):
    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_sueldos')  # o donde quieras redirigir
    else:
        form = TrabajadorForm()
    return render(request, 'registrar_trabajador.html', {'form': form})

def listar_trabajadores(request):
    trabajadores = Trabajador.objects.all()
    return render(request, 'listar_trabajadores.html', {'trabajadores': trabajadores})

def editar_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id=trabajador_id)
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, instance=trabajador)
        if form.is_valid():
            form.save()
            return redirect('listar_trabajadores')
    else:
        form = TrabajadorForm(instance=trabajador)
    return render(request, 'editar_trabajador.html', {'form': form, 'trabajador': trabajador})

def eliminar_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id=trabajador_id)
    trabajador.delete()
    return redirect('listar_trabajadores')