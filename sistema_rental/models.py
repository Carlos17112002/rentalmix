from django.db import models

# Create your models here.

from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombre} ({self.rut})"
    
# models.py
from django.db import models

class Producto(models.Model):
    descripcion = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    precio_costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateField()
    ultima_compra = models.DateField(null=True, blank=True)
    proveedor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.descripcion} ({self.codigo})"

class Factura(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('parcial', 'Parcial'),
        ('pagada', 'Pagada'),
    ]
    mes = models.CharField(max_length=7)  # Ej: "2025-07"
    fecha = models.DateField()
    numero = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    mensaje = models.CharField(max_length=200, blank=True, null=True)
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_pago = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Factura {self.numero} - {self.mes}"

class Cotizacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cotización de {self.cliente} - {self.monto}"

class Compra(models.Model):
    factura = models.CharField(max_length=50)
    proveedor = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    # Si se requieren detalles por producto, se puede definir un modelo intermedio y usar ManyToManyField

    def __str__(self):
        return f"Compra {self.factura} - {self.proveedor}"

class Pago(models.Model):
    mes = models.CharField(max_length=7)  # Ej: "2025-07"
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.mes} - {self.total}"

class ExpectedIncome(models.Model):
    mes = models.CharField(max_length=7)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Proyección {self.mes} - {self.total}"
    
    
from django.db import models

class Cotizacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    total_neto = models.PositiveIntegerField()
    total_iva = models.PositiveIntegerField()
    total_final = models.PositiveIntegerField()

    def __str__(self):
        return f"Cotización #{self.id} - {self.fecha.strftime('%d/%m/%Y')}"

class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='detalles')
    producto = models.CharField(max_length=255)
    codigo = models.CharField(max_length=50)
    precio_unitario = models.PositiveIntegerField()
    cantidad = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    iva = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
    
from django.contrib.auth.models import User
class Compra2(models.Model):
    fecha = models.DateField()
    factura = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=100)
    creada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class ProductoCompra(models.Model):
    compra = models.ForeignKey(Compra2, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    neto = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
from django.db import models

class CompraCamiones(models.Model):
    mes = models.CharField(max_length=10)
    fecha = models.DateField()
    factura = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    mensaje = models.TextField(blank=True, null=True)
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('Pendiente', 'Pendiente'),
        ('Pagado', 'Pagado'),
        ('Vencido', 'Vencido'),
    ])

    def __str__(self):
        return f"Compra {self.factura} - {self.mes}"


class VentaCamiones(models.Model):
    mes = models.CharField(max_length=10)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Venta {self.mes} - {self.total}"


class PagoCamiones(models.Model):
    mes = models.CharField(max_length=10)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Pago {self.mes} - {self.total}"