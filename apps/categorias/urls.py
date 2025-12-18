from django.urls import path
from apps.categorias import views

app_name = 'categorias'

urlpatterns = [
    path('', views.listado_categorias, name='listado_categorias'),
    path('registrar_categorias/', views.registrar_categorias, name='registrar_categorias'),
    path('editar_categorias/<int:pk_id>/', views.editar_categorias, name='editar_categorias'),
    path('eliminar_categorias/<int:pk_id>/', views.eliminar_categorias, name='eliminar_categorias'),
]