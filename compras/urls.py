from django.urls import path
from . import views

urlpatterns = [
    path('subir-libro/', views.subir_libro_sii, name='subir_libro'),
    path('facturas/', views.listar_facturas, name='listar_facturas'),
    path('pagar-factura/<int:factura_id>/', views.pagar_factura, name='pagar_factura'),
    path('actualizar_montos/', views.actualizar_montos_facturas, name='actualizar_montos'),


]