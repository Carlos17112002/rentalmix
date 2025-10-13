from django.db import models

# Create your models here.
from django.db import models

class RegistroOtro(models.Model):
    TIPO_CHOICES = [
        ('cotizacion', 'Cotización'),
        ('ajuste', 'Ajuste'),
        ('nota', 'Nota interna'),
        ('gasto', 'Gasto menor'),
        ('otro', 'Otro'),
        ('patente', 'Patente'),
        ('licencia', 'Licencia'),
        ('mantenimiento', 'Mantenimiento'),
        ('servicio', 'Servicio'),
        ('suscripcion', 'Suscripción'),
        ('impuesto', 'Impuesto'),
        ('multas', 'Multas'),
        ('seguros', 'Seguros'),
        ('honorarios', 'Honorarios'),
        ('comisiones', 'Comisiones'),
        ('publicidad', 'Publicidad'),
        ('viajes', 'Viajes'),
        ('capacitación', 'Capacitación'),
        ('otros', 'Otros'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    documento = models.FileField(upload_to='documentos_otros/', blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.fecha} - ${self.monto or 0:,.0f}"