from django.db import models
from django.contrib.auth.models import User

class PerfilCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    # Tarjeta (solo últimos 4 dígitos, nunca el número completo)
    tarjeta_ultimos4 = models.CharField(max_length=4, blank=True, null=True)
    tarjeta_nombre = models.CharField(max_length=100, blank=True, null=True)
    tarjeta_vencimiento = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField(blank=True, default="")
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def precio_clp(self):
        # 2500 -> "2.500" (formato de miles chileno)
        return f"{self.precio:,}".replace(",", ".")


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('preparando', 'Preparando'),
        ('entregado', 'Entregado'),
    ]

    PAGO_CHOICES = [
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
        ('efectivo', 'Efectivo'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_cliente = models.CharField(max_length=100, blank=True, null=True)
    metodo_pago = models.CharField(max_length=20, choices=PAGO_CHOICES)
    subtotal = models.IntegerField()
    total = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    creado_en = models.DateTimeField(auto_now_add=True)
    direccion_entrega = models.CharField(max_length=200, blank=True, null=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    correo_invitado = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    cantidad = models.IntegerField(default=1)
