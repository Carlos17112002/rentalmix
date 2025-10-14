from django.urls import path
from .views import index, crear_cliente, crear_producto, listar_clientes, listar_productos, consulta_codigo, cotizaciones
from .views import ingreso_compra, gardilcic, consulta_compra, orden_compra, menu_facturas, menu_rental
from .views import menu_informes, editar_cliente, eliminar_cliente, eliminar_producto, editar_producto, costos_fijos_2025, costos_fijos_2024
from . import views

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
    path('menu_informes/', menu_informes, name='menu_informes'),
    path('clientes/editar/<int:id>/', editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', eliminar_cliente, name='eliminar_cliente'),
    path('eliminar_producto/<int:id>/', eliminar_producto, name='eliminar_producto'),
    path('editar_producto/<int:id>/', editar_producto, name='editar_producto'),
    path('guardar_cotizacion/', views.guardar_cotizacion, name='guardar_cotizacion'),
    path('costos_fijos_2025', costos_fijos_2025, name='costos_fijos_2025'),
    path('costos_fijos_2024', costos_fijos_2024, name='costos_fijos_2024')
    

]