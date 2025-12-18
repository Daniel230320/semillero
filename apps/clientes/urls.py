from django.urls import path
from apps.clientes import views

app_name = 'clientes'

urlpatterns = [
    path('', views.listado_clientes, name="listado_clientes"),
    path('registrar_clientes/', views.registrar_clientes, name="registrar_clientes"),
    path('editar_clientes/<int:pk_id>/', views.editar_clientes, name="editar_clientes"),
    path('eliminar_clientes/<int:pk_id>/', views.eliminar_clientes, name="eliminar_clientes"),
    path('detalle_cliente/<int:pk_id>/', views.detalle_cliente, name="detalle_cliente"),
]