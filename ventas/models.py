from django.db import models

# Create your models here.
from django.db import models

class Venta(models.Model):
    fecha = models.DateField()
    cliente = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    pagado = models.BooleanField(default=False)
    documento = models.FileField(upload_to='documentos_ventas/', blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"Venta a {self.cliente} el {self.fecha} - ${self.total:,.0f} ({estado})"