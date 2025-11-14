from django.urls import path
from . import views

urlpatterns = [
    path('contrato/nuevo/', views.crear_contrato, name='crear_contrato'),
    path('contrato/<int:contrato_id>/', views.detalle_contrato, name='detalle_contrato'),
    path('contrato/<int:contrato_id>/estado_pago/nuevo/', views.crear_estado_pago, name='crear_estado_pago'),
    path('dashboard/', views.dashboard_camion, name='dashboard_camion'),
    path('dashboard/<int:camion_id>/', views.dashboard_camion, name='dashboard_camion'),
    path('camion/nuevo/', views.crear_camion, name='camion'),
    path('camiones/', views.listar_camion, name='listar_camiones'),
    path('estado-pago/nuevo/<int:camion_id>/', views.crear_estado_pago_completo, name='crear_estado_pago_completo'),
    path('camion/<int:camion_id>/editar/', views.editar_camion, name='camion_editar'),
    path('camion/<int:camion_id>/eliminar/', views.eliminar_camion, name='camion_eliminar'),
    path('estados-pago/', views.ver_estados_pago, name='ver_estados_pago'),
    path('estado-pago/<int:estado_id>/', views.detalle_estado_pago, name='detalle_estado_pago'),

]