from django import forms
from .models import ProductoCompra

class ProductoCompradoForm(forms.ModelForm):
    class Meta:
        model = ProductoCompra
        fields = ['descripcion', 'compra', 'precio_unitario', 'cantidad']