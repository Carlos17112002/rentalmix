from django.urls import path
from . import views


urlpatterns = [
    path('camiones/', views.dashboard_camiones, name='dashboard_camiones'),
    path('camiones/<int:camion_id>/', views.dashboard_camiones, name='dashboard_camiones'),
    path('camiones/agregar/', views.agregar_camion, name='agregar_camion'),
    path('camiones/<int:camion_id>/detalle/', views.camion_detalle, name='camion_detalle'),
    path('camion/<int:camion_id>/contrato/nuevo/', views.crear_contrato, name='crear_contrato'),
    path('contrato/<int:contrato_id>/', views.detalle_contrato, name='detalle_contratos'),
    path('contrato/<int:contrato_id>/editar/', views.editar_contrato, name='editar_contrato'),
    path('contrato/<int:contrato_id>/eliminar/', views.eliminar_contrato, name='eliminar_contrato'),
]