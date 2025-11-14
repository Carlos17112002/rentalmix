from django.db import models
class LibroVenta(models.Model):
    fecha = models.DateField(help_text="Fecha del libro de ventas")
    archivo = models.FileField(upload_to='libros_ventas/')
    
    def __str__(self):
        return f"Libro de ventas {self.fecha}"


class FacturaVenta(models.Model):
    folio = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateField()
    cliente = models.CharField(max_length=100)
    rut_cliente = models.CharField(max_length=20)
    monto_exento = models.FloatField(default=0)
    monto_neto = models.FloatField(default=0)
    monto_iva = models.FloatField(default=0)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    pagada = models.BooleanField(default=False)
    fecha_pago = models.DateField(blank=True, null=True)
    libro = models.ForeignKey(LibroVenta, on_delete=models.SET_NULL, null=True, blank=True, related_name='facturas')
    comprobante = models.FileField(upload_to='comprobantes_ventas/', null=True, blank=True)
    boucher_pago = models.FileField(upload_to='bouchers_pagos_ventas/', null=True, blank=True)
    origen_libro = models.CharField(max_length=50, blank=True, null=True)
    


    def __str__(self):
        return f"Venta {self.folio} - {self.cliente}"