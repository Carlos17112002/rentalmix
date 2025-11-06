from django.db import models

class FacturaCompra(models.Model):
    folio = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateField()
    proveedor = models.CharField(max_length=100)
    rut_proveedor = models.CharField(max_length=12)  # Nuevo campo para RUT del proveedor
    monto_exento = models.FloatField(default=0)
    monto_neto = models.FloatField(default=0)
    monto_iva = models.FloatField(default=0)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    pagada = models.BooleanField(default=False)
    fecha_pago = models.DateField(blank=True, null=True)
    origen_libro = models.DateField()  # Fecha en que se subió el libro
    fecha_pago = models.DateField(blank=True, null=True)
    comprobante = models.FileField(upload_to='comprobantes_compras/', null=True, blank=True)
    boucher_pago = models.FileField(upload_to='bouchers_pagos_compras/', null=True, blank=True)


    def __str__(self):
        return f"Factura {self.folio} - {self.proveedor}"

from django.db import models

class LibroCompra(models.Model):
    fecha = models.DateField(help_text="Fecha del libro subido")
    archivo = models.FileField(upload_to='libros/', help_text="Archivo original del libro CSV")

    def __str__(self):
        return f"Libro {self.fecha}"
    
