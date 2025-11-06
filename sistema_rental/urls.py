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
    path('costos_fijos_2024', costos_fijos_2024, name='costos_fijos_2024'),
    path('cst_fijos', views.prueba_cst_fijos, name='prueba'),
    path('ordenes/', views.listar_ordenes, name='listar_ordenes'),
    path('productos/importar/', views.importar_productos, name='importar_productos'),
    path('clientes/importar/', views.importar_clientes, name='importar_clientes'),
    path('ordenes/eliminar/<int:orden_id>/', views.eliminar_orden, name='eliminar_orden'),
    path('editar_compra/<int:producto_id>/', views.editar_compra, name='editar_compra'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('costos_fijos_detallados/', views.costos_fijos_detallados, name='costos_fijos_detallados'),
    path('listado_cotizaciones', views.listado_cotizaciones, name='listado_cotizaciones'),
    path('detalle_orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('salida_producto/', views.salida_producto, name='salida_producto'),
    path('disminuir_producto/<int:producto_id>/', views.disminuir_producto, name='disminuir_producto'),
    path('cotizacion/<int:cotizacion_id>/detalles/', views.detalles_cotizacion, name='detalles_cotizacion'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('ver_usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    

    
]