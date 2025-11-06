from django.urls import path
from . import views

urlpatterns = [
    path('sueldos/', views.listar_sueldos, name='listar_sueldos'),
    path('sueldos/agregar/', views.agregar_sueldo, name='agregar_sueldo'),
    path('sueldos/editar/<int:sueldo_id>/', views.editar_sueldo, name='editar_sueldo'),
    path('sueldos/pagar/<int:sueldo_id>/', views.pagar_sueldo, name='pagar_sueldo'),
    path('sueldos/eliminar/<int:sueldo_id>/', views.eliminar_sueldo, name='eliminar_sueldo'),
    path('trabajadores/registrar/', views.crear_trabajador, name='registrar_trabajador'),
    path('trabajadores/', views.listar_trabajadores, name='listar_trabajadores'),
    path('trabajadores/editar/<int:trabajador_id>/', views.editar_trabajador, name='editar_trabajador'),
    path('trabajadores/eliminar/<int:trabajador_id>/', views.eliminar_trabajador, name='eliminar_trabajador'),
    
]