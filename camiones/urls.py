from django.urls import path
from . import views


urlpatterns = [
    path('camiones/', views.dashboard_camiones, name='dashboard_camiones'),
    path('camiones/<int:camion_id>/', views.dashboard_camiones, name='camion_detalle'),
    path('camiones/agregar/', views.agregar_camion, name='agregar_camion'),
    path('camiones/<int:camion_id>/detalle/', views.camion_detalle, name='camion_detalle'),
]