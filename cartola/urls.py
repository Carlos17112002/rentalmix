from django.urls import path
from . import views

urlpatterns = [
    path('cartola_filtrada/', views.cartola_filtrada, name='cartola'),
]