from django import forms
from .models import Trabajador

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'apellido', 'rut', 'fecha_contrato']  # ajusta según tu modelo
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_contrato': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }