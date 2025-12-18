from django.urls import path
from apps.usuarios import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.listado_usuarios, name='listado_usuarios'),
    path('registrar_usuarios/', views.registrar_usuarios, name='registrar_usuarios'),
    path('editar_usuarios/<int:pk_id>/', views.editar_usuarios, name='editar_usuarios'),
    path('eliminar_usuarios/<int:pk_id>/', views.eliminar_usuarios, name='eliminar_usuarios'),
    path('detalle_usuario/<int:pk_id>/', views.detalle_usuario, name="detalle_usuario"),

    path('cuenta_perfil/', views.cuenta_perfil, name="cuenta_perfil"),
]