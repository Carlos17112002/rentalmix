from django.urls import path
from . import views

urlpatterns = [
    path('ventas/subir/', views.subir_libro_ventas, name='subir_libro_ventas'),
    path('ventas/', views.listar_ventas, name='listar_ventas'),
    path('cobrar/<int:venta_id>/', views.cobrar_venta, name='cobrar_venta'),
    path('actualizar_montos_ventas/', views.actualizar_montos_ventas, name='actualizar_montos_ventas'),
]