from django.urls import path
from .views import index, crear_cliente, crear_producto, listar_clientes, listar_productos, consulta_codigo, cotizaciones
from .views import ingreso_compra, gardilcic, consulta_compra, orden_compra, menu_facturas, menu_rental
from .views import menu_informes

urlpatterns = [
    path('', index, name='index'),
    path('clientes/nuevo/', crear_cliente, name='creacion_cliente'),
    path('productos/nuevo/', crear_producto, name='crear_producto'),
    path('clientes/', listar_clientes, name='base_datos'),
    path('productos/', listar_productos, name='listar_productos'),
    path('consulta_codigo/', consulta_codigo, name='consulta_codigo'),
    path('cotizaciones/', cotizaciones, name='cotizaciones'),
    path('ingreso_compra/', ingreso_compra, name='ingreso_compra'),
    path('gardilcic/', gardilcic, name='gardilcic'),
    path('consulta_compra/', consulta_compra, name='consulta_compra'),
    path('orden_compra/', orden_compra, name='orden_compra'),
    path('menu_facturas', menu_facturas, name='menu_facturas'),
    path('menu_rentalmix', menu_rental, name='menu_rental'),
    path('menu_informes/', menu_informes, name='menu_informes')
]