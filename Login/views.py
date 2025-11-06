from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings


def login_view(request):
    error = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contraseña = request.POST.get('contraseña')

        user = authenticate(request, username=nombre, password=contraseña)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige al menú principal
        else:
            error = "Usuario o contraseña incorrectos."

    return render(request, 'login.html', {'error': error})


from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def menu_principal(request):
    return render(request, 'index.html') 


def recuperar_contraseña(request):
    mensaje = None
    if request.method == 'POST':
        correo = request.POST.get('correo')
        # Aquí podrías verificar si el correo existe en tu modelo Usuario
        # y generar un token de recuperación real
        send_mail(
            'Recuperación de contraseña - RENTAL MIX',
            'Haz clic en el siguiente enlace para restablecer tu contraseña: https://tusitio.com/restablecer',
            settings.DEFAULT_FROM_EMAIL,
            [correo],
            fail_silently=False,
        )
        mensaje = "Se han enviado instrucciones a tu correo."

    return render(request, 'recuperar_contraseña.html', {'mensaje': mensaje})


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # ← redirige al login después de cerrar sesión
