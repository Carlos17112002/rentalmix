from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_otro, name='registrar_otro'),
    path('listar/', views.listar_otros, name='listar_otros'),
]