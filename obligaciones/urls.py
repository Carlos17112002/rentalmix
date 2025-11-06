from django.urls import path
from . import views

urlpatterns = [
    path('pagos/f29/', views.pagos_f29, name='pagos_f29'),
    path('pagos/previred/', views.pagos_previred, name='pagos_previred'),
]