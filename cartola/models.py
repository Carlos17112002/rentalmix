from django.db import models

# cartola/models.py
from django.db import models

class SaldoInicialMensual(models.Model):
    año = models.IntegerField()
    mes = models.IntegerField()
    monto = models.DecimalField(max_digits=12, decimal_places=2,null=False, default=0)

    class Meta:
        unique_together = ('año', 'mes')

    def __str__(self):
        return f"{self.mes}/{self.año}: ${self.monto}"