from django.contrib import admin
from .models import Producto,PerfilCliente    #<--- importas los dashboard al admin

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "categoria", "disponible")
    list_filter = ("categoria", "disponible")
    search_fields = ("nombre", "categoria")


@admin.register(PerfilCliente)
class PerfilClienteAdmin(admin.ModelAdmin):
    list_display = ("user", "telefono", "fecha_nacimiento")
    search_fields = ("user__username", "user__email", "telefono")