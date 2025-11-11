from django.db import models

# Create your models here.
class Camion(models.Model):
    patente = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.PositiveIntegerField()
    capacidad_kg = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])
    observaciones = models.TextField(blank=True)

from django.db import models

class EstadoPagoCamion(models.Model):
    camion = models.ForeignKey('Camion', on_delete=models.CASCADE, related_name='estados_pago')
    periodo = models.CharField(max_length=20)

    # Sección: Base
    anticipo = models.PositiveIntegerField(default=0)
    avance_a_la_fecha = models.PositiveIntegerField(default=0)
    estado_pago_anterior = models.PositiveIntegerField(default=0)
    presente_estado_pago = models.PositiveIntegerField(default=0)

    # Ajustes
    devolucion_anticipo = models.PositiveIntegerField(default=0)
    descuentos_multas = models.PositiveIntegerField(default=0)

    # Anticipos
    saldo_anterior_anticipo = models.PositiveIntegerField(default=0)
    devolucion_seguro = models.PositiveIntegerField(default=0)
    nuevo_saldo_anticipo = models.PositiveIntegerField(default=0)

    # Subtotales y descuentos
    subtotal = models.PositiveIntegerField(default=0)
    descuento_especial = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # porcentaje
    subtotal_con_descuento = models.PositiveIntegerField(default=0)
    iva = models.PositiveIntegerField(default=0)
    total_estado_pago = models.PositiveIntegerField(default=0)

    # Retenciones
    saldo_anterior_retenciones = models.PositiveIntegerField(default=0)
    retencion = models.PositiveIntegerField(default=0)
    devolucion_retenciones = models.PositiveIntegerField(default=0)
    nuevo_saldo_retenciones = models.PositiveIntegerField(default=0)

    # Total final
    total_a_pagar = models.PositiveIntegerField(default=0)

    fecha_emision = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Estado de Pago {self.periodo} - Camión {self.camion.patente}"

class ArriendoCamion(models.Model):
    camion = models.ForeignKey(Camion, on_delete=models.CASCADE, related_name='arriendos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    valor_por_dia = models.PositiveIntegerField()

    @property
    def dias_arriendo(self):
        return (self.fecha_fin - self.fecha_inicio).days + 1

    @property
    def total(self):
        return self.dias_arriendo * self.valor_por_dia

from django.db import models


class Contrato(models.Model):
    camion = models.ForeignKey(Camion, on_delete=models.CASCADE, related_name='contratos')
    nombre = models.CharField(max_length=100, help_text="Nombre o referencia del contrato")
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    valor_dia = models.PositiveIntegerField(help_text="Valor diario del arriendo en CLP")
    numero_local = models.PositiveIntegerField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    @property
    def dias_arriendo(self):
        return (self.fecha_termino - self.fecha_inicio).days + 1

    @property
    def total_arriendo(self):
        return self.dias_arriendo * self.valor_dia

    def __str__(self):
        return f"Contrato #{self.id} - {self.nombre}"