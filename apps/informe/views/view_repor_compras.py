from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from apps.empresa.models import *
from apps.informe.filters import *
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from django.template.loader import get_template
from django.db.models import Sum
from datetime import datetime
import os
from django.conf import settings

# Vista Consultar Reporte Compras
@login_required
@permission_required('empresa.generar_reportes', raise_exception=True)
def reporte_compras(request):
    compras_filter = ReporteComprasFilter(request.GET, queryset=Compras.objects.all())
    return render(request, 'informe_informes/reporte_compras.html', {'compras_filter': compras_filter,})


# Generar PDF Reporte Compras
def generar_pdf_compra(self, request):
    """ Método para generar el PDF a partir de un template HTML. """
    # Obtener valores
    compras = Compras.objects.all()
    compras_filter = ReporteComprasFilter(request.GET, compras)
    empresa = Empresas.objects.get(idempresa=100)
    logo_url = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None # uso al no estar desplegado
    #logo_url = f"file://{os.path.join(settings.MEDIA_ROOT, empresa.logo.name)}" if empresa.logo else None # uso al estar desplegado
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    totales = compras_filter.qs.aggregate(subtotal_general=Sum('subtotal'), iva_general=Sum('valoriva'), total_general=Sum('total'),)

    # Obtener valores fecha desde hasta
    fecha_compra_desde = datetime.strptime(request.GET.get('fecha_compra_desde', ''), '%Y-%m-%d').date() if request.GET.get('fecha_compra_desde', '') else None
    fecha_compra_hasta = datetime.strptime(request.GET.get('fecha_compra_hasta', ''), '%Y-%m-%d').date() if request.GET.get('fecha_compra_hasta', '') else None
    user = CustomUser.objects.get(id=int(request.GET.get('user'))) if request.GET.get('user') else None
    proveedor = Proveedores.objects.get(idproveedor=int(request.GET.get('idproveedor'))) if request.GET.get('idproveedor') else None

    # Pasar los valores al contexto
    context = {'empresa': empresa, 'compras': compras_filter.qs, 'logo_url': logo_url, 'now': now, 'totales': totales,
        'fecha_compra_desde': fecha_compra_desde, 'fecha_compra_hasta': fecha_compra_hasta, 'user': user, 'proveedor': proveedor,
    }

    template_path = 'informe_pdf/compras.html' # Renderizar el template HTML
    template = get_template(template_path)
    html = template.render(context)
    # Generar el PDF
    result = BytesIO()
    HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(result)
    return result.getvalue()


# Vista Genera PDF Reporte Compras
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('empresa.generar_reportes', raise_exception=True), name='dispatch')
class GenerarPDFComprasView(View):
    def get(self, request, descargar, *args, **kwargs):
        pdf_content = generar_pdf_compra(self, request)
        if pdf_content:
            filename = "ReporteCompras.pdf"  # Nombre del archivo PDF
            response = HttpResponse(pdf_content, content_type='application/pdf')
            if descargar == 'True':
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            else:
                response['Content-Disposition'] = f'filename="{filename}"'
            return response
        else:
            return HttpResponse("Error al generar el PDF.", status=500)
