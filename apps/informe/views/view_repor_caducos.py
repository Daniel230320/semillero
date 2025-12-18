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

# Vista Consultar Reporte Productos Caducos
@login_required
@permission_required('empresa.generar_reportes', raise_exception=True)
def reporte_caducos(request):
    caducos_filter = ReporteProductosCaducosFilter(request.GET, queryset=Lotes.objects.filter(codigoarticulo__tiene_fecha_caduca=True))
    return render(request, 'informe_informes/reporte_caducos.html', {'caducos_filter': caducos_filter,})

# Generar PDF Reporte Productos Caducos
def generar_pdf_caducos(self, request):
    """ Método para generar el PDF a partir de un template HTML. """
    # Obtener valores
    lotes = Lotes.objects.filter(codigoarticulo__tiene_fecha_caduca=True)
    caducos_filter = ReporteProductosCaducosFilter(request.GET, queryset=lotes)
    empresa = Empresas.objects.get(idempresa=100)
    logo_url = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None # uso al no estar desplegado
    #logo_url = f"file://{os.path.join(settings.MEDIA_ROOT, empresa.logo.name)}" if empresa.logo else None # uso al estar desplegado
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Obtener valores de request.GET
    producto = Articulos.objects.get(idarticulo=int(request.GET.get('descripcion_articulo'))) if request.GET.get('descripcion_articulo') else None
    categoria = Categoriaarticulos.objects.get(idcategoriaarticulo=int(request.GET.get('idcategoriaarticulo'))) if request.GET.get('idcategoriaarticulo') else None
    estado_lote = Estado_lotes.objects.get(idestado_lote=int(request.GET.get('idestado_lote'))) if request.GET.get('idestado_lote') else None

    # Obtener valores fecha desde hasta
    fecha_caducidad_desde = datetime.strptime(request.GET.get('fecha_caducidad_desde', ''), '%Y-%m-%d').date() if request.GET.get('fecha_caducidad_desde', '') else None
    fecha_caducidad_hasta = datetime.strptime(request.GET.get('fecha_caducidad_hasta', ''), '%Y-%m-%d').date() if request.GET.get('fecha_caducidad_hasta', '') else None

    # Pasar los valores al contexto
    context = {'empresa': empresa, 'producto': producto, 'categoria': categoria, 'caducos': caducos_filter.qs, 'logo_url': logo_url, 
        'estado_lote': estado_lote,'now': now, 'fecha_caducidad_desde': fecha_caducidad_desde, 'fecha_caducidad_hasta': fecha_caducidad_hasta,
    }

    template_path = 'informe_pdf/productos_caducos.html' # Renderizar el template HTML
    template = get_template(template_path)
    html = template.render(context)
    # Generar el PDF
    result = BytesIO()
    HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(result)
    return result.getvalue()

# Vista Genera PDF Reporte Productos Caducos
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('empresa.generar_reportes', raise_exception=True), name='dispatch')
class GenerarPDFCaducosView(View):
    def get(self, request, descargar, *args, **kwargs):
        pdf_content = generar_pdf_caducos(self, request)
        if pdf_content:
            filename = "ReporteProductosCaducos.pdf"  # Nombre del archivo PDF
            response = HttpResponse(pdf_content, content_type='application/pdf')
            if descargar == 'True':
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            else:
                response['Content-Disposition'] = f'filename="{filename}"'
            return response
        else:
            return HttpResponse("Error al generar el PDF.", status=500)
        
        