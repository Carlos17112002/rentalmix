from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import PagoF29, PagoPreviRed

def pagos_f29(request):
    if request.method == 'POST':
        PagoF29.objects.create(
            monto=request.POST.get('monto'),
            fecha_pago=request.POST.get('fecha_pago'),
            comprobante=request.FILES.get('comprobante')
        )
        return redirect('pagos_f29')

    pagos = PagoF29.objects.all().order_by('-fecha_pago')
    return render(request, 'pagos_f29.html', {'pagos': pagos})


def pagos_previred(request):
    if request.method == 'POST':
        PagoPreviRed.objects.create(
            monto=request.POST.get('monto'),
            fecha_pago=request.POST.get('fecha_pago'),
            comprobante=request.FILES.get('comprobante')
        )
        return redirect('pagos_previred')

    pagos = PagoPreviRed.objects.all().order_by('-fecha_pago')
    return render(request, 'pagos_previred.html', {'pagos': pagos})