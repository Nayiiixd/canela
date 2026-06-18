from django.shortcuts import render
from .models import Producto, PerfilCliente # <-- para añadir al dashboard
#funciones para login y register funcionen
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages


# Create your views here.
#funciones simples para que se vean los html
def index(request):
    return render(request, "appcanela/index.html")

def menu(request):
    return render(request, "appcanela/menu.html")

def nosotros(request):
    return render(request, "appcanela/nosotros.html")

def carrito(request):
    return render(request, "appcanela/carrito.html")


def confirmacion(request):
    return render(request, "appcanela/confirmacion.html")


#funcion para productos en bd
def menu(request):
    productos = Producto.objects.filter(disponible=True)
    return render(request, "appcanela/menu.html", {
        "productos": productos
    })

#funciones de registro y login

def registro(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        fecha_nacimiento = request.POST.get("fecha_nacimiento") or None
        password = request.POST.get("password", "").strip()

        if not nombre or not correo or not password:
            messages.error(request, "Debes completar nombre, correo y contraseña.")
            return redirect("registro")

        if User.objects.filter(username=correo).exists():
            messages.error(request, "Ya existe una cuenta con ese correo.")
            return redirect("registro")

        usuario = User.objects.create_user(
            username=correo,
            email=correo,
            password=password,
            first_name=nombre
        )

        PerfilCliente.objects.create(
            user=usuario,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento
        )

        auth_login(request, usuario)
        messages.success(request, "Cuenta creada correctamente.")
        return redirect("index")

    return render(request, "appcanela/registro.html")


def login_view(request):
    if request.method == "POST":
        correo = request.POST.get("correo", "").strip()
        password = request.POST.get("password", "").strip()

        usuario = authenticate(request, username=correo, password=password)

        if usuario is not None:
            auth_login(request, usuario)
            messages.success(request, "Sesión iniciada correctamente.")
            return redirect("index")
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect("login")

    return render(request, "appcanela/login.html")


def logout_view(request):
    auth_logout(request)
    return redirect("index")