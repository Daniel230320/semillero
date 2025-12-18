from django.urls import path
from apps.articulos import views

app_name = 'articulos'

urlpatterns = [
    path('', views.listado_articulos, name='listado_articulos'),
    path('registrar_productos/', views.registrar_articulos, name='registrar_articulos'),
    path('editar_productos/<int:pk_id>/', views.editar_articulos, name='editar_articulos'),
    path('eliminar_productos/<int:pk_id>/', views.eliminar_articulos, name='eliminar_articulos'),
    path('detalle_productos/<int:pk_id>/', views.detalle_articulos, name="detalle_articulos"),
]