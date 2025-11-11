from django.urls import path
from . import views


urlpatterns = [
    path('camiones/', views.dashboard_camiones, name='dashboard_camiones'),
    path('camiones/<int:camion_id>/', views.dashboard_camiones, name='camion_detalle'),
    path('camiones/agregar/', views.agregar_camion, name='agregar_camion'),
    path('camiones/<int:camion_id>/detalle/', views.camion_detalle, name='camion_detalle'),
    path('camion/<int:camion_id>/contrato/nuevo/', views.crear_contrato, name='crear_contrato'),
    path('contrato/<int:contrato_id>/', views.detalle_contrato, name='detalle_contrato'),
]