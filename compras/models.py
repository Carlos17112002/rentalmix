from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class LibroCompra(models.Model):
    ESTADO_CHOICES = [
        ('procesando', 'Procesando'),
        ('correcto', 'Correctamente procesado'),
        ('error', 'Error al procesar'),
    ]

    fecha = models.DateField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    pagado = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='libros_compras/')
    nombre_archivo = models.CharField(max_length=255, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='procesando')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Libro {self.fecha} - ${self.total:,.0f} ({self.get_estado_display()})"