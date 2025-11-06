from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import LibroCompra, FacturaCompra

class LibroCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'archivo', 'facturas_asociadas')
    list_filter = ('fecha',)
    search_fields = ('fecha',)
    readonly_fields = ('archivo',)

    def facturas_asociadas(self, obj):
        return FacturaCompra.objects.filter(origen_libro=obj.fecha).count()
    facturas_asociadas.short_description = 'Facturas asociadas'

    def has_add_permission(self, request):
        # Permitir subir libros desde el admin si lo deseas
        return True

    def has_delete_permission(self, request, obj=None):
        # Permitir eliminar libros desde el admin
        return True

admin.site.register(LibroCompra, LibroCompraAdmin)