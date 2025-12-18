from django.urls import path
from apps.ventas.views import view_create, view_detail, view_list, view_pdf

app_name = 'ventas'

urlpatterns = [
    path('', view_list.listado_ventas, name='listado_ventas'),
    path('registrar_ventas/', view_create.registrar_ventas, name='registrar_ventas'),
    path('detalle_ventas/<int:pk_id>/', view_detail.detalle_ventas, name="detalle_ventas"),

    path('factura/<int:pk_id>/', view_pdf.FacturaPDFView.as_view(), name='vista_factura'),
    path('ticket/<int:pk_id>/', view_pdf.TicketPDFView.as_view(), name='vista_ticket'),
]