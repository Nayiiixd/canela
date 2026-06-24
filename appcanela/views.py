from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Pedido, ItemPedido, Producto, PerfilCliente

def index(request):
    return render(request, 'appcanela/index.html')

def menu(request):
    productos = Producto.objects.filter(disponible=True)
    return render(request, 'appcanela/menu.html', {'productos': productos})

def nosotros(request):
    return render(request, 'appcanela/nosotros.html')

def carrito(request):
    return render(request, 'appcanela/carrito.html')

def login_view(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        try:
            user_obj = User.objects.get(email=correo)
        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
            return redirect("login")
        user = authenticate(request, username=user_obj.username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get("next", "index"))
        else:
            messages.error(request, "Contraseña incorrecta")
    return render(request, 'appcanela/login.html')

@require_POST
def logout_view(request):
    logout(request)
    return redirect("index")

def registro(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        fecha = request.POST.get("fecha_nacimiento")
        password = request.POST.get("password")
        username = correo
        if User.objects.filter(username=username).exists():
            messages.info(request, "El usuario ya existe")
            return redirect("registro")
        user = User.objects.create_user(
            username=username,
            email=correo,
            password=password,
            first_name=nombre
        )
        PerfilCliente.objects.create(
            user=user,
            telefono=telefono,
            fecha_nacimiento=fecha if fecha else None
        )
        login(request, user)
        return redirect("index")
    return render(request, 'appcanela/registro.html')

@require_POST
def procesar_pedido(request):
    metodo_pago = request.POST.get("metodo_pago")

    try:
        subtotal = int(request.POST.get("subtotal", 0))
        total = int(request.POST.get("total", 0))
        num_items = int(request.POST.get("num_items", 0))
    except ValueError:
        messages.error(request, "Datos inválidos en el pedido.")
        return redirect("carrito")

    direccion = request.POST.get("direccion", "").strip()
    fecha_entrega = request.POST.get("fecha_entrega") or None
    correo_invitado = request.POST.get("correo_invitado", "").strip()
    nombre_invitado = request.POST.get("nombre_invitado", "").strip()

    pedido = Pedido.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        nombre_cliente=request.user.first_name if request.user.is_authenticated else nombre_invitado,
        metodo_pago=metodo_pago,
        subtotal=subtotal,
        total=total,
        direccion_entrega=direccion,
        fecha_entrega=fecha_entrega,
        correo_invitado=correo_invitado if not request.user.is_authenticated else None,
    )
    for i in range(num_items):
        nombre = request.POST.get(f"item_nombre_{i}")
        precio = request.POST.get(f"item_precio_{i}")
        cantidad = request.POST.get(f"item_qty_{i}")
        if nombre and precio and cantidad:
            ItemPedido.objects.create(
                pedido=pedido,
                nombre=nombre,
                precio=int(precio),
                cantidad=int(cantidad)
            )
    request.session['ultimo_pedido_id'] = pedido.id
    return redirect("simulacion_pago")


def confirmacion(request):
    return render(request, 'appcanela/confirmacion.html')

@login_required
def perfil(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-creado_en').prefetch_related('items')
    return render(request, 'appcanela/perfil.html', {'pedidos': pedidos})


@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-creado_en').prefetch_related('items')
    return render(request, 'appcanela/mis_pedidos.html', {'pedidos': pedidos})

@user_passes_test(lambda u: u.is_staff)
def panel_admin(request):
    hoy = timezone.now().date()
    pedidos_hoy = Pedido.objects.filter(creado_en__date=hoy)
    ventas_hoy = pedidos_hoy.aggregate(Sum("total"))["total__sum"] or 0
    context = {
        "pedidos_hoy_count": pedidos_hoy.count(),
        "ventas_hoy": ventas_hoy,
        "total_clientes": User.objects.count(),
        "productos": Producto.objects.all(),
        "ultimos_pedidos": Pedido.objects.order_by("-creado_en")[:5],
        "todos_pedidos": Pedido.objects.all().order_by("-creado_en"),
    }
    return render(request, 'appcanela/panel_admin.html', context)

@user_passes_test(lambda u: u.is_staff)
@require_POST
def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    nuevo_estado = request.POST.get("estado")
    if nuevo_estado in ["pendiente", "preparando", "entregado"]:
        pedido.estado = nuevo_estado
        pedido.save()
    return redirect("panel_admin")


CATEGORIAS_PRODUCTO = [
    ("clasicos", "Clásicos"),
    ("chocolate", "Chocolate"),
    ("premium", "Premium"),
    ("especiales", "Especiales"),
]


@user_passes_test(lambda u: u.is_staff)
def producto_nuevo(request):
    if request.method == "POST":
        Producto.objects.create(
            nombre=request.POST.get("nombre"),
            categoria=request.POST.get("categoria"),
            precio=int(request.POST.get("precio") or 0),
            descripcion=request.POST.get("descripcion", ""),
            disponible=request.POST.get("estado") == "activo",
            imagen=request.FILES.get("imagen"),
        )
        return redirect("panel_admin")
    return render(request, "appcanela/producto_form.html", {
        "accion": "Nuevo producto",
        "categorias": CATEGORIAS_PRODUCTO,
    })


@user_passes_test(lambda u: u.is_staff)
def producto_editar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.categoria = request.POST.get("categoria")
        producto.precio = int(request.POST.get("precio") or 0)
        producto.descripcion = request.POST.get("descripcion", "")
        producto.disponible = request.POST.get("estado") == "activo"
        if request.FILES.get("imagen"):
            producto.imagen = request.FILES.get("imagen")
        producto.save()
        return redirect("panel_admin")
    return render(request, "appcanela/producto_form.html", {
        "accion": "Editar producto",
        "producto": producto,
        "categorias": CATEGORIAS_PRODUCTO,
    })


@user_passes_test(lambda u: u.is_staff)
@require_POST
def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect("panel_admin")

def simulacion_pago(request):
    pedido_id = request.session.get('ultimo_pedido_id')
    pedido = get_object_or_404(Pedido, id=pedido_id) if pedido_id else None
    perfil = None
    if request.user.is_authenticated:
        perfil, _ = PerfilCliente.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        resultado = request.POST.get('resultado', 'aprobado')

        # Guardar nombre del invitado
        if not request.user.is_authenticated and pedido:
            nombre_invitado = request.POST.get('nombre_invitado', '').strip()
            if nombre_invitado:
                pedido.nombre_cliente = nombre_invitado
                pedido.save()

        # Guardar tarjeta si es usuario registrado
        if request.user.is_authenticated and perfil and resultado == 'aprobado':
            guardar = request.POST.get('guardar_tarjeta')
            num = request.POST.get('num_tarjeta', '').replace(' ', '')
            if guardar and len(num) >= 4:
                perfil.tarjeta_ultimos4 = num[-4:]
                perfil.tarjeta_nombre = request.POST.get('nombre_tarjeta', '')
                perfil.tarjeta_vencimiento = request.POST.get('vencimiento', '')
                perfil.save()

        return render(request, 'appcanela/pago_resultado.html', {
            'pedido': pedido,
            'resultado': resultado,
        })

    return render(request, 'appcanela/simulacion_pago.html', {
        'pedido': pedido,
        'perfil': perfil,
    })