from django.contrib import admin
from .models import Pedido, ItemPedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_cliente', 'metodo_pago', 'total', 'estado', 'creado_en')
    list_filter = ('estado', 'metodo_pago', 'creado_en')
    search_fields = ('nombre_cliente',)



@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'nombre', 'precio', 'cantidad')