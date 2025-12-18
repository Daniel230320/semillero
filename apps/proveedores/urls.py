from django.urls import path
from apps.proveedores import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.listado_proveedores, name="listado_proveedores"),
    path('registrar_proveedores/', views.registrar_proveedores, name="registrar_proveedores"),
    path('editar_proveedores/<int:pk_id>/', views.editar_proveedores, name="editar_proveedores"),
    path('eliminar_proveedores/<int:pk_id>/', views.eliminar_proveedores, name="eliminar_proveedores"),
    path('detalle_proveedor/<int:pk_id>/', views.detalle_proveedor, name="detalle_proveedor"),
]