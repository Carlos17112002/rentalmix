from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_otro, name='registrar_otro'),
    path('listar/', views.listar_otros, name='listar_otros'),
    path('otros/editar/<int:id>/', views.editar_otro, name='editar_otro'),
    path('otros/eliminar/<int:id>/', views.eliminar_otro, name='eliminar_otro'),
]