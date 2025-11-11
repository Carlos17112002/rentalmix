from django.contrib import admin
from .models import Compra2, ProductoCompra, OrdenCompra, DetalleOrden, ProductoNuevo

# Inline para productos dentro de Compra2
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
    list_filter = ('iva_porcentaje',)
    search_fields = ('descripcion',)

# Inline para productos dentro de OrdenCompra
class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 0
    readonly_fields = ('producto', 'producto_nuevo', 'cantidad', 'precio_unitario', 'total')
    can_delete = False

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'fecha', 'cliente', 'neto', 'iva', 'total')
    list_filter = ('fecha',)
    search_fields = ('numero', 'cliente')
    inlines = [DetalleOrdenInline]

@admin.register(DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden', 'producto', 'producto_nuevo', 'cantidad', 'precio_unitario', 'total')
    list_filter = ('orden',)
    search_fields = ('producto__descripcion', 'producto_nuevo__descripcion')

@admin.register(ProductoNuevo)
class ProductoNuevoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')