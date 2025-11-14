from django.db import models

# Create your models here.

from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombre} ({self.rut})"
    
# models.py
from django.db import models

from django.db import models

class Producto(models.Model):
    descripcion = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    precio_costo_unitario = models.DecimalField(max_digits=10, decimal_places=0)
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
    neto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_compra = models.DateField(null=True, blank=True)
    ultima_compra = models.DateField(null=True, blank=True)
    proveedor = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField(default=1)
    factura = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.descripcion} ({self.codigo})"


class ProductoNuevo(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=255)
    precio_costo_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateField()
    ultima_compra = models.DateField(null=True, blank=True)
    proveedor = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class OrdenCompra(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    fecha = models.DateField()
    cliente = models.CharField(max_length=100)
    neto = models.IntegerField()
    iva = models.IntegerField()
    total = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.numero:
            ultimo = OrdenCompra.objects.order_by('-numero').first()
            self.numero = (ultimo.numero + 1) if ultimo else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OC-{self.numero:05d} ({self.fecha})"
    
class DetalleOrden(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, null=True, blank=True, on_delete=models.SET_NULL)
    producto_nuevo = models.ForeignKey(ProductoNuevo, null=True, blank=True, on_delete=models.SET_NULL)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.orden} - {self.producto or self.producto_nuevo}"
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
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    total_neto = models.PositiveIntegerField()
    total_iva = models.PositiveIntegerField()
    total_final = models.PositiveIntegerField()

    def __str__(self):
        return f"Cotización #{self.id} - {self.cliente} - {self.fecha.strftime('%d/%m/%Y')}"

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


from datetime import date

class ProductoCompra(models.Model):
    compra = models.ForeignKey(Compra2, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50)
    fecha_compra = models.DateField(default=date.today)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
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
    pagado = models.DecimalField(max_digits=12, decimal_places=0, default=0)
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
    
# models.py

class NumeroOrdenDisponible(models.Model):
    numero = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"N° {self.numero} disponible"

