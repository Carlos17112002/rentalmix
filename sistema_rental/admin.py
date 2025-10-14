from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Compra2, ProductoCompra

class ProductoCompraInline(admin.TabularInline):
    model = ProductoCompra
    extra = 0
    readonly_fields = ('descripcion', 'cantidad', 'precio_unitario', 'iva_porcentaje', 'neto', 'impuesto', 'total')
    can_delete = False

@admin.register(Compra2)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'factura', 'proveedor')
    list_filter = ('proveedor', 'fecha')
    search_fields = ('factura', 'proveedor')
    inlines = [ProductoCompraInline]

@admin.register(ProductoCompra)
class ProductoCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'compra', 'cantidad', 'precio_unitario', 'iva_porcentaje', 'total')
    list_filter = ('iva_porcentaje',)  # ✅ solo campos que existen en ProductoCompra
    search_fields = ('descripcion',)