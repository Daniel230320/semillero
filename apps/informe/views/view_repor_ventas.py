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

# Vista Consultar Reporte Ventas
@login_required
@permission_required('empresa.generar_reportes', raise_exception=True)
def reporte_ventas(request):
    ventas_filter = ReporteVentasFilter(request.GET, queryset=Ventas.objects.all())
    return render(request, 'informe_informes/reporte_ventas.html', {'ventas_filter': ventas_filter,})


# Generar PDF Reporte Ventas
def generar_pdf_venta(self, request):
    """ Método para generar el PDF a partir de un template HTML. """
    # Obtener valores
    ventas = Ventas.objects.all()
    ventas_filter = ReporteVentasFilter(request.GET, ventas)
    empresa = Empresas.objects.get(idempresa=100)
    logo_url = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None # uso al no estar desplegado
    #logo_url = f"file://{os.path.join(settings.MEDIA_ROOT, empresa.logo.name)}" if empresa.logo else None # uso al estar desplegado
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    totales = ventas_filter.qs.aggregate(subtotal_general=Sum('subtotal'), descuento_general=Sum('descuento'), iva_general=Sum('valoriva'), total_general=Sum('total'),)
    
    # Obtener valores request.GET
    fecha_venta_desde = datetime.strptime(request.GET.get('fecha_venta_desde', ''), '%Y-%m-%d').date() if request.GET.get('fecha_venta_desde', '') else None
    fecha_venta_hasta = datetime.strptime(request.GET.get('fecha_venta_hasta', ''), '%Y-%m-%d').date() if request.GET.get('fecha_venta_hasta', '') else None
    user = CustomUser.objects.get(id=int(request.GET.get('user'))) if request.GET.get('user') else None
    cliente = Clientes.objects.get(idcliente=int(request.GET.get('idcliente'))) if request.GET.get('idcliente') else None

    # Pasar los valores al contexto
    context = {'empresa': empresa, 'ventas': ventas_filter.qs, 'logo_url': logo_url, 'now': now, 'totales': totales,
        'fecha_venta_desde': fecha_venta_desde, 'fecha_venta_hasta': fecha_venta_hasta, 'user': user, 'cliente': cliente,
    }

    template_path = 'informe_pdf/ventas.html' # Renderizar el template HTML
    template = get_template(template_path)
    html = template.render(context)
    # Generar el PDF
    result = BytesIO()
    HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(result)
    return result.getvalue()


# Vista Genera PDF Reporte Ventas
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('empresa.generar_reportes', raise_exception=True), name='dispatch')
class GenerarPDFVentasView(View):
    def get(self, request, descargar, *args, **kwargs):
        pdf_content = generar_pdf_venta(self, request)
        if pdf_content:
            # Configurar la respuesta HTTP para servir el PDF con nombre dinámico
            filename = "ReporteVentas.pdf"  # Nombre del archivo PDF
            response = HttpResponse(pdf_content, content_type='application/pdf')
            if descargar == 'True':
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            else:
                response['Content-Disposition'] = f'filename="{filename}"'
            return response
        else:
            return HttpResponse("Error al generar el PDF.", status=500)
            
