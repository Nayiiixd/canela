from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('nosotros/', views.nosotros, name='nosotros'),

   
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),

   
    path('carrito/', views.carrito, name='carrito'),
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),

    # Usuario
    path('perfil/', views.perfil, name='perfil'),

    # Admin
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('panel-admin/pedido/<int:pedido_id>/estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
]