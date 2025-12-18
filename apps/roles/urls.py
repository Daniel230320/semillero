from django.urls import path
from apps.roles import views

app_name = 'roles'

urlpatterns = [
    path('', views.roles, name="roles"),
    path('eliminar_roles/<int:pk_id>/', views.eliminar_roles, name='eliminar_roles'),
    path('registrar_roles/', views.registrar_roles, name='registrar_roles'),
    path('editar_roles/<int:pk_id>/', views.editar_roles, name="editar_roles"),
    path('permiso_roles/<int:pk_id>/', views.permiso_roles, name="permiso_roles"),
]