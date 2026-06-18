from django.contrib import admin
from django.urls import path
from django.urls import include, path
from .views import index, menu, nosotros,carrito,confirmacion,registro, login_view, logout_view

urlpatterns = [
    path("", index, name="index"),
    path("menu/", menu, name="menu"),
    path("nosotros/", nosotros, name="nosotros"),
    path("carrito/", carrito, name="carrito"),
    path("registro/",registro, name="registro"),
    path("confirmacion/",confirmacion, name="confirmacion"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]