from django.urls import path
from apps.compras.views import view_create, view_detail, view_list

app_name = 'compras'

urlpatterns = [
    path('', view_list.listado_compras, name='listado_compras'),
    path('registrar_compras/', view_create.registrar_compras, name='registrar_compras'),
    path('detalle_compras/<int:pk_id>/', view_detail.detalle_compras, name="detalle_compras"),
]