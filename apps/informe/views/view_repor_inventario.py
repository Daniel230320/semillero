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
from django.db.models import Sum, F
from datetime import datetime
import os
from django.conf import settings

# Vista Consultar Reporte Inventario
@login_required
@permission_required('empresa.generar_reportes', raise_exception=True)
def reporte_inventario(request):
    inventarios_filter = ReporteInventarioFilter(request.GET, queryset=Articulos.objects.all())
    return render(request, 'informe_informes/reporte_inventario.html', {'inventarios_filter': inventarios_filter})


# Generar PDF Reporte Inventario con WeasyPrint
def generar_pdf_inventario(self, request):
    """ Método para generar el PDF a partir de un template HTML usando WeasyPrint. """
    # Obtener Valores (igual que antes)
    inventarios = (Articulos.objects.values('codigoarticulo', 'descripcion_articulo', 'idcategoriaarticulo__descripcion_categoriaarticulo', 'stock', 'stock_minimo', 'stock_maximo', 'costo')
        .annotate(total=Sum(F('stock') * F('costo'))).order_by('-stock')
    )
    inventarios_filter = ReporteInventarioFilter(request.GET, queryset=inventarios) 
    empresa = Empresas.objects.get(idempresa=100)
    logo_url = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None # uso al no estar desplegado
    #logo_url = f"file://{os.path.join(settings.MEDIA_ROOT, empresa.logo.name)}" if empresa.logo else None # uso al estar desplegado
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    totales = inventarios_filter.qs.aggregate(costo_general=Sum('costo'), total_general=Sum('total'),)

    # Obtener valores de request.GET
    descripcion_articulo = Articulos.objects.get(idarticulo=int(request.GET.get('descripcion_articulo'))) if request.GET.get('descripcion_articulo') else None
    idcategoriaarticulo = Categoriaarticulos.objects.get(idcategoriaarticulo=int(request.GET.get('idcategoriaarticulo'))) if request.GET.get('idcategoriaarticulo') else None

    # Pasar los valores al contexto
    context = {'empresa': empresa, 'inventarios': inventarios_filter.qs, 'logo_url': logo_url, 'now': now, 
        'descripcion_articulo': descripcion_articulo, 'idcategoriaarticulo': idcategoriaarticulo, 'totales': totales,
    }

    template_path = 'informe_pdf/inventarios.html' # Renderizar el template HTML
    template = get_template(template_path)
    html = template.render(context)
    
    # Generar el PDF con WeasyPrint
    result = BytesIO()
    HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(result)
    return result.getvalue()

# Vista Genera PDF Reporte Inventario (igual que antes)
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('empresa.generar_reportes', raise_exception=True), name='dispatch')
class GenerarPDFInventariosView(View):
    def get(self, request, descargar, *args, **kwargs):
        pdf_content = generar_pdf_inventario(self, request)
        if pdf_content:
            # Configurar la respuesta HTTP para servir el PDF con nombre dinámico
            filename = "ReporteInventarios.pdf"  # Nombre del archivo PDF
            response = HttpResponse(pdf_content, content_type='application/pdf')
            if descargar == 'True':
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            else:
                response['Content-Disposition'] = f'filename="{filename}"'
            return response
        else:
            return HttpResponse("Error al generar el PDF.", status=500)