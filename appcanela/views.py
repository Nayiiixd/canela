from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "appcanela/index.html")

def menu(request):
    return render(request, "appcanela/menu.html")

def nosotros(request):
    return render(request, "appcanela/nosotros.html")


def carrito(request):
    return render(request, "appcanela/carrito.html")

def registro(request):
    return render(request, "appcanela/registro.html")

def confirmacion(request):
    return render(request, "appcanela/confirmacion.html")

def registro(request):
    return render(request, "appcanela/registro.html")

def login_view(request):
    return render(request, "appcanela/login.html")