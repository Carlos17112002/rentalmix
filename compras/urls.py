from django.urls import path
from . import views

urlpatterns = [
    path('subir-libro/', views.subir_libro_compras, name='subir_libro_compras'),
    path('listar/', views.listar_compras, name='listar_compras'),
    path('revisar/<int:libro_id>/', views.revisar_libro, name='revisar_libro'),
    path('eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('pagar/<int:libro_id>/', views.seleccionar_banco, name='pagar_libro'),
    

]