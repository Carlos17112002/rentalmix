from django.db import models

# Create your models here.
class PagoF29(models.Model):
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_pago = models.DateField()
    comprobante = models.FileField(upload_to='comprobantes_f29/', null=True, blank=True)

    def __str__(self):
        return f"F29 - ${self.monto} - {self.fecha_pago}"


class PagoPreviRed(models.Model):
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_pago = models.DateField()
    comprobante = models.FileField(upload_to='comprobantes_previred/', null=True, blank=True)

    def __str__(self):
        return f"PreviRed - ${self.monto} - {self.fecha_pago}"