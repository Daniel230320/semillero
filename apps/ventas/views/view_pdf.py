from django.contrib.auth.decorators import login_required, permission_required
from apps.ventas.models import Ventas, Detalle_ventas, Pagos
from apps.empresa.models import Empresas
from django.db.models import Sum, Q
from django.http import HttpResponse
from weasyprint import HTML, CSS
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from django.utils.decorators import method_decorator
from django.conf import settings
from apps.articulos.models import TipoArticulos
from django.utils import timezone

# Generar detalle nutricional por comestible y no comestible
def generar_distribucion_consolidada(idventa):
    try:
        # Obtener tipos de artículos una sola vez
        tipo_comestible = TipoArticulos.objects.get(idtipoarticulo=1)
        tipo_no_comestible = TipoArticulos.objects.get(idtipoarticulo=2)
        
        # Definir los filtros especiales
        filtros = {
            'general': Q(),
            'azucar': Q(codigoarticulo__idnivelazucar__valor_nivel__gte=1),
            'grasas': Q(codigoarticulo__idnivelgrasa__valor_nivel__gte=1),
            'sal': Q(codigoarticulo__idnivelsal__valor_nivel__gte=1)
        }
        
        # Estructura para almacenar todos los datos (solo unidades ahora)
        resultados = {
            'general': {'com': 0, 'ncom': 0},
            'azucar': {'com': 0, 'ncom': 0}, 
            'grasas': {'com': 0, 'ncom': 0},
            'sal': {'com': 0, 'ncom': 0}
        }
        
        # Procesar cada filtro
        for filtro, q_filtro in filtros.items():
            # Comestibles
            detalles_com = Detalle_ventas.objects.filter(
                idventa=idventa,
                codigoarticulo__idtipoarticulo=tipo_comestible.idtipoarticulo
            ).filter(q_filtro)
            
            resultados[filtro]['com'] = detalles_com.aggregate(total=Sum('cantidad'))['total'] or 0
            
            # No comestibles
            detalles_ncom = Detalle_ventas.objects.filter(
                idventa=idventa,
                codigoarticulo__idtipoarticulo=tipo_no_comestible.idtipoarticulo
            ).filter(q_filtro)
            
            resultados[filtro]['ncom'] = detalles_ncom.aggregate(total=Sum('cantidad'))['total'] or 0
        
        # Calcular totales generales
        total_unidades = resultados['general']['com'] + resultados['general']['ncom']
        
        # Construir la tabla consolidada (solo con unidades)
        tabla = [
            # Fila Comestibles
            {
                'indicador': 'Comestibles',
                'general': f"{resultados['general']['com']}",
                'azucar': f"{resultados['azucar']['com']}" if resultados['azucar']['com'] > 0 else "0",
                'grasa': f"{resultados['grasas']['com']}" if resultados['grasas']['com'] > 0 else "0",
                'sal': f"{resultados['sal']['com']}" if resultados['sal']['com'] > 0 else "0",
                'total': f"{resultados['general']['com']}"
            },
            # Fila No Comestibles
            {
                'indicador': 'No Comestibles',
                'general': f"{resultados['general']['ncom']}",
                'azucar': f"{resultados['azucar']['ncom']}" if resultados['azucar']['ncom'] > 0 else "0",
                'grasa': f"{resultados['grasas']['ncom']}" if resultados['grasas']['ncom'] > 0 else "0",
                'sal': f"{resultados['sal']['ncom']}" if resultados['sal']['ncom'] > 0 else "0",
                'total': f"{resultados['general']['ncom']}"
            },
            # Separador
            {'tipo': 'separador'},
            # Total Unidades (eliminada la fila de Total Productos)
            {
                'indicador': 'TOTAL UNIDADES',
                'general': f"{resultados['general']['com'] + resultados['general']['ncom']}",
                'azucar': f"{resultados['azucar']['com'] + resultados['azucar']['ncom']}",
                'grasa': f"{resultados['grasas']['com'] + resultados['grasas']['ncom']}" if (resultados['grasas']['com'] + resultados['grasas']['ncom']) > 0 else "0",
                'sal': f"{resultados['sal']['com'] + resultados['sal']['ncom']}" if (resultados['sal']['com'] + resultados['sal']['ncom']) > 0 else "0",
                'total': f"{resultados['general']['com'] + resultados['general']['ncom']}"
            },
            # Porcentajes
            {
                'indicador': 'PORCENTAJE',
                'general': "100.0%",
                'azucar': f"{(resultados['azucar']['com'] + resultados['azucar']['ncom']) / total_unidades * 100:.1f}%" if total_unidades > 0 else "0.0%",
                'grasa': f"{(resultados['grasas']['com'] + resultados['grasas']['ncom']) / total_unidades * 100:.1f}%" if total_unidades > 0 and (resultados['grasas']['com'] + resultados['grasas']['ncom']) > 0 else "0.0%",
                'sal': f"{(resultados['sal']['com'] + resultados['sal']['ncom']) / total_unidades * 100:.1f}%" if total_unidades > 0 and (resultados['sal']['com'] + resultados['sal']['ncom']) > 0 else "0.0%",
                'total': "100%"
            }
        ]
        
        return tabla
        
    except Exception as e:
        return f"Error: {str(e)}"
     
# Generar detalle nutricional por indicadores
def generar_indicadores_nutricionales(idventa):
    try:
        # Definir los niveles nutricionales
        NIVELES = [
            {'nombre': 'No contiene', 'valor': 0},
            {'nombre': 'Bajo', 'valor': 1},
            {'nombre': 'Medio', 'valor': 2},
            {'nombre': 'Alto', 'valor': 3}
        ]
        
        # Obtener todos los detalles de la venta
        detalles = Detalle_ventas.objects.filter(idventa=idventa).select_related(
            'codigoarticulo__idnivelazucar',
            'codigoarticulo__idnivelsal',
            'codigoarticulo__idnivelgrasa'
        )
        
        # Inicializar estructura de resultados para cantidades
        resultados = {
            'azucar': {nivel['valor']: {'cantidad': 0, 'porcentaje': 0} for nivel in NIVELES},
            'sal': {nivel['valor']: {'cantidad': 0, 'porcentaje': 0} for nivel in NIVELES},
            'grasa': {nivel['valor']: {'cantidad': 0, 'porcentaje': 0} for nivel in NIVELES},
            'total_cantidad': 0
        }
        
        # Procesar cada detalle contando las cantidades exactas
        for detalle in detalles:
            cantidad = detalle.cantidad
            resultados['total_cantidad'] += cantidad
            
            # Contar por nivel de azúcar
            nivel_azucar = detalle.codigoarticulo.idnivelazucar.valor_nivel if detalle.codigoarticulo.idnivelazucar else 0
            resultados['azucar'][nivel_azucar]['cantidad'] += cantidad
            
            # Contar por nivel de sal
            nivel_sal = detalle.codigoarticulo.idnivelsal.valor_nivel if detalle.codigoarticulo.idnivelsal else 0
            resultados['sal'][nivel_sal]['cantidad'] += cantidad
            
            # Contar por nivel de grasa
            nivel_grasa = detalle.codigoarticulo.idnivelgrasa.valor_nivel if detalle.codigoarticulo.idnivelgrasa else 0
            resultados['grasa'][nivel_grasa]['cantidad'] += cantidad
        
        # Calcular porcentajes basados en cantidades
        for categoria in ['azucar', 'sal', 'grasa']:
            for nivel in resultados[categoria]:
                resultados[categoria][nivel]['porcentaje'] = (
                    resultados[categoria][nivel]['cantidad'] / resultados['total_cantidad'] * 100
                    if resultados['total_cantidad'] > 0 else 0
                )
        
        # Construir la tabla consolidada mostrando solo cantidades
        tabla = []
        for nivel in NIVELES:
            fila = {
                'nivel': nivel['nombre'],
                'azucar': resultados['azucar'][nivel['valor']]['cantidad'],
                'azucar_porcentaje': f"{resultados['azucar'][nivel['valor']]['porcentaje']:.1f}%",
                'sal': resultados['sal'][nivel['valor']]['cantidad'],
                'sal_porcentaje': f"{resultados['sal'][nivel['valor']]['porcentaje']:.1f}%",
                'grasa': resultados['grasa'][nivel['valor']]['cantidad'],
                'grasa_porcentaje': f"{resultados['grasa'][nivel['valor']]['porcentaje']:.1f}%",
                'total': (
                    resultados['azucar'][nivel['valor']]['cantidad'] + 
                    resultados['sal'][nivel['valor']]['cantidad'] + 
                    resultados['grasa'][nivel['valor']]['cantidad']
                )
            }
            tabla.append(fila)
        
        # Agregar fila de totales basada en cantidades
        tabla.append({
            'nivel': 'TOTAL',
            'azucar': resultados['total_cantidad'],
            'azucar_porcentaje': '100%',
            'sal': resultados['total_cantidad'],
            'sal_porcentaje': '100%',
            'grasa': resultados['total_cantidad'],
            'grasa_porcentaje': '100%',
            'total': resultados['total_cantidad'] * 3
        })
        
        return {
            'tabla': tabla,
            'total_cantidad': resultados['total_cantidad']
        }
        
    except Exception as e:
        return {'error': f"Error al generar indicadores: {str(e)}"}

# Vista Factura
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ventas.ver_ventas', raise_exception=True), name='dispatch')
class FacturaPDFView(View):
    def get(self, request, pk_id):
        # Obtener datos
        venta = Ventas.objects.get(idventa=pk_id)
        pago = Pagos.objects.get(idventa=pk_id)
        venta_detalles = Detalle_ventas.objects.filter(idventa=pk_id)
        total_cantidad = Detalle_ventas.objects.filter(idventa=pk_id).aggregate(total_cantidad=Sum('cantidad'))['total_cantidad']
        empresa = Empresas.objects.get(idempresa=100)
        logo_url = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None # uso al no estar desplegado
        #logo_url = f"file://{os.path.join(settings.MEDIA_ROOT, empresa.logo.name)}" if empresa.logo else None # uso al estar desplegado

        # Renderizar la plantilla y generar el PDF
        template_path = 'pdf/factura_template.html'
        template = get_template(template_path)
        html = template.render({ 
            'empresa': empresa, 'venta': venta, 'venta_detalles': venta_detalles,
            'total_cantidad': total_cantidad, 'pago': pago, 'cambio': pago.monto-venta.total, 'logo_url': logo_url,
            'distribucion_consolidada': generar_distribucion_consolidada(pk_id),
            'indicadores_nutricionales': generar_indicadores_nutricionales(pk_id)
        })

        # Crear el PDF
        result = BytesIO()
        HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(result)
        
        # Retornar el PDF
        filename = f"factura_{pk_id}.pdf"
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{filename}"'
        return response

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('ventas.ver_ventas', raise_exception=True), name='dispatch')
class TicketPDFView(View):
    def get(self, request, pk_id):
        try:
            # Obtener datos
            venta = Ventas.objects.get(idventa=pk_id)
            pago = Pagos.objects.get(idventa=pk_id)
            venta_detalles = Detalle_ventas.objects.filter(idventa=pk_id)
            total_cantidad = Detalle_ventas.objects.filter(idventa=pk_id).aggregate(total_cantidad=Sum('cantidad'))['total_cantidad']
            empresa = Empresas.objects.get(idempresa=100)
            logo_url = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None

            # Manejo seguro de la fecha
            fecha_display = venta.fecha_venta
            if not hasattr(venta.fecha_venta, 'hour'):
                fecha_display = timezone.datetime.combine(venta.fecha_venta, timezone.datetime.min.time())

            # Generar datos nutricionales simplificados
            distribucion = generar_distribucion_consolidada(pk_id)
            indicadores = generar_indicadores_nutricionales(pk_id)
            
            # Simplificar datos para el ticket
            distribucion_simplificada = [fila for fila in distribucion if fila.get('tipo') != 'separador']
            indicadores_simplificados = {
                'tabla': [fila for fila in indicadores['tabla'] if fila['nivel'] != 'TOTAL']
            }

            # Renderizar la plantilla del ticket
            template = get_template('pdf/ticket_template.html')
            html = template.render({
                'empresa': empresa, 'venta': venta, 'fecha_display': fecha_display,
                'venta_detalles': venta_detalles, 'total_cantidad': total_cantidad,
                'pago': pago, 'cambio': pago.monto - venta.total, 'logo_url': logo_url,
                'distribucion_consolidada': distribucion_simplificada,
                'indicadores_nutricionales': indicadores_simplificados
            })
            
            # Generar PDF
            result = BytesIO()
            HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(result)
            
            # Retornar el PDF
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="ticket_{pk_id}.pdf"'
            return response

        except Exception as e:
            return HttpResponse(f"Error al generar el ticket: {str(e)}", status=500)