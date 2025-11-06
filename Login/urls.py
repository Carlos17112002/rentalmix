# urls.py
from django.urls import path
from .views import login_view, menu_principal, recuperar_contraseña, logout_view

urlpatterns = [
    path('', login_view, name='login'),
    path('menu/', menu_principal, name='menu_principal'),
    path('recuperar/', recuperar_contraseña, name='recuperar_contraseña'),
    path('logout/', logout_view, name='logout'),




]