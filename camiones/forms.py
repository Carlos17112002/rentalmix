from django import forms
from .models import Camion

class CamionForm(forms.ModelForm):
    class Meta:
        model = Camion
        fields = ['patente', 'marca', 'modelo', 'año', 'capacidad_kg', 'estado', 'observaciones']
        widgets = {
            'estado': forms.Select(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')]),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

from django import forms
from .models import ArriendoCamion

class ArriendoCamionForm(forms.ModelForm):
    class Meta:
        model = ArriendoCamion
        fields = ['fecha_inicio', 'fecha_fin', 'valor_por_dia']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }