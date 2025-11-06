from django.db import models

class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    fecha_contrato = models.DateField()

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

class Sueldo(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, related_name='sueldos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    pagado = models.BooleanField(default=False)
    documento = models.FileField(upload_to='sueldos_documentos/', null=True, blank=True)

    def __str__(self):
        return f"{self.trabajador.nombre} - {self.monto} - {self.fecha_pago}"