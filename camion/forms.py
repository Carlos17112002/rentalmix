from django import forms
from .models import Contrato, EstadoPago

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['camion', 'nombre', 'periodo', 'uf_pactada', 'uf_del_dia', 'fecha_inicio', 'fecha_termino']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'}),
            'periodo': forms.TextInput(attrs={'placeholder': 'Ej: 01-11-2025 al 30-11-2025'}),
            'uf_pactada': forms.NumberInput(attrs={'step': '0.01'}),
            'uf_del_dia': forms.NumberInput(attrs={'step': '0.01'}),
        }

class EstadoPagoForm(forms.ModelForm):
    class Meta:
        model = EstadoPago
        fields = ['avance_a_la_fecha', 'estado_pago_anterior', 'devolucion_seguro']

from .models import Camion

class CamionForm(forms.ModelForm):
    class Meta:
        model = Camion
        fields = ['subcontrato', 'obras']
        widgets = {
            'obras': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Ej: Obra 212 DIAMANTE, Obra 305 ALTO MAIPO'
            }),
        }

from django import forms
from .models import EstadoPago

class EstadoPagoCompletoForm(forms.ModelForm):
    class Meta:
        model = EstadoPago
        fields = [
            'obra',
            'fecha_inicio', 'fecha_termino',
            'uf_pactada', 'uf_del_dia',
            'avance_a_la_fecha', 'estado_pago_anterior', 'devolucion_seguro'
        ]
        widgets = {
            'obra': forms.TextInput(attrs={'placeholder': 'Ej: Obra 212 DIAMANTE'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'}),
            'uf_pactada': forms.NumberInput(attrs={'step': '0.01'}),
            'uf_del_dia': forms.NumberInput(attrs={'step': '0.01'}),
            'avance_a_la_fecha': forms.NumberInput(),
            'estado_pago_anterior': forms.NumberInput(),
            'devolucion_seguro': forms.NumberInput(),
        }