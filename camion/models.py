from django.db import models

# Create your models here.
from django.db import models
from django.db.models import Max

class Contrato(models.Model):
    camion = models.ForeignKey('Camion', on_delete=models.CASCADE, related_name='contratos')
    nombre = models.CharField(max_length=100, help_text="Nombre o referencia del contrato")
    periodo = models.CharField(max_length=50, help_text="Ej: 01-11-2025 al 30-11-2025")
    uf_pactada = models.DecimalField(max_digits=10, decimal_places=2)
    uf_del_dia = models.DecimalField(max_digits=10, decimal_places=2)
    orden_compra = models.PositiveIntegerField(null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.orden_compra is None:
            ultimo = Contrato.objects.aggregate(max_oc=Max('orden_compra'))['max_oc'] or 0
            self.orden_compra = ultimo + 1
        super().save(*args, **kwargs)

    @property
    def dias_arriendo(self):
        return (self.fecha_termino - self.fecha_inicio).days + 1

    @property
    def valor_total(self):
        return float(self.uf_pactada) * float(self.uf_del_dia)

    @property
    def valor_dia(self):
        return round(self.valor_total / self.dias_arriendo, 2) if self.dias_arriendo > 0 else 0

    def __str__(self):
        return f"Contrato {self.orden_compra} - {self.nombre}"
    
class Camion(models.Model):
    subcontrato = models.CharField(max_length=100)
    obras = models.TextField(default="Sin obra asignada")

    def lista_obras(self):
        return [obra.strip() for obra in self.obras.split(',') if obra.strip()]
    
from django.db import models
from django.db.models import Max
from .models import Camion
import datetime

class EstadoPago(models.Model):
    camion = models.ForeignKey(Camion, on_delete=models.CASCADE, related_name='estados_pago')
    obra = models.CharField(max_length=100)

    fecha_inicio = models.DateField(default=datetime.date(2023, 1, 1))
    fecha_termino = models.DateField(default=datetime.date(2023, 1, 1))
    uf_pactada = models.DecimalField(max_digits=10, decimal_places=2)
    uf_del_dia = models.DecimalField(max_digits=10, decimal_places=2)

    avance_a_la_fecha = models.PositiveIntegerField()
    estado_pago_anterior = models.PositiveIntegerField()
    devolucion_seguro = models.PositiveIntegerField()

    creado = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def dias_arriendo(self):
        return (self.fecha_termino - self.fecha_inicio).days + 1

    @property
    def valor_total(self):
        return float(self.uf_pactada) * float(self.uf_del_dia)

    @property
    def valor_dia(self):
        return round(self.valor_total / self.dias_arriendo, 2) if self.dias_arriendo > 0 else 0

    @property
    def presente_estado_pago(self):
        return round(self.valor_total)

    @property
    def subtotal(self):
        return self.presente_estado_pago - self.devolucion_seguro

    @property
    def iva(self):
        return round(self.subtotal * 0.19)

    @property
    def total_estado_pago(self):
        return self.subtotal + self.iva

    def __str__(self):
        return f"Estado de Pago - Camión {self.camion.subcontrato} - Obra {self.obra}"