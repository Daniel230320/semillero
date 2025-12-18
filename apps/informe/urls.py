from django.urls import path
from apps.informe.views import view_repor_compras, view_repor_inventario, view_repor_kardex, view_repor_ventas, view_principal
from apps.informe.views import view_repor_caducos

app_name = 'informe'

urlpatterns = [
    # url vistas consultar reportes
    path('', view_principal.reporte_inicio, name="reporte_inicio"),
    path('reporte_ventas/', view_repor_ventas.reporte_ventas, name="reporte_ventas"),
    path('reporte_compras/', view_repor_compras.reporte_compras, name="reporte_compras"),
    path('reporte_inventario/', view_repor_inventario.reporte_inventario, name="reporte_inventario"),
    path('reporte_kardex/', view_repor_kardex.reporte_kardex, name="reporte_kardex"),
    path('reporte_productos_caducos/', view_repor_caducos.reporte_caducos, name="reporte_caducos"),

    # url ajax
    path('get-productos/', view_principal.get_productos_por_categoria, name='get_productos_por_categoria'),
    path('get-caducos/', view_principal.get_caducos_por_categoria, name='get_caducos_por_categoria'),
    
    # url generar reportes pdf
    path('generar-pdf-ventas/<str:descargar>/', view_repor_ventas.GenerarPDFVentasView.as_view(), name='generar_pdf_ventas'),
    path('generar-pdf-compras/<str:descargar>/', view_repor_compras.GenerarPDFComprasView.as_view(), name='generar_pdf_compras'),
    path('generar-pdf-inventarios/<str:descargar>/', view_repor_inventario.GenerarPDFInventariosView.as_view(), name='generar_pdf_inventarios'),
    path('generar-pdf-kardex/<str:descargar>/', view_repor_kardex.GenerarPDFKardexView.as_view(), name='generar_pdf_kardex'),
    path('generar-pdf-caducos/<str:descargar>/', view_repor_caducos.GenerarPDFCaducosView.as_view(), name='generar_pdf_caducos'),
]
