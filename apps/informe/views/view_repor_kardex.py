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
from django.db.models import Sum, F, Value
from datetime import datetime
from collections import deque
from decimal import Decimal, ROUND_HALF_UP
import os
from django.conf import settings

# Vista Consultar Reporte Kardex
@login_required
@permission_required('empresa.generar_reportes', raise_exception=True)
def reporte_kardex(request):
    productos = Articulos.objects.all().order_by('descripcion_articulo')
    return render(request, 'informe_informes/reporte_kardex.html', {'productos': productos})


# Obtener Kardex
def kardex_articulo(id_articulo, metodo):
    # Obtener las compras y ventas para el artículo especificado
    compras = Detalle_compras.objects.filter(codigoarticulo__codigoarticulo=id_articulo).annotate(
        fecha_movimiento=F('idcompra__fecha_compra'),
        concepto=F('idcompra__concepto'),
        idtipomovimiento_id=Value(1)  # 1 para compras
    ).values('fecha_movimiento', 'concepto', 'cantidad', 'preciounitario', 'valor', 'idtipomovimiento_id')

    ventas = Detalle_ventas.objects.filter(codigoarticulo__codigoarticulo=id_articulo).annotate(
        fecha_movimiento=F('idventa__fecha_venta'),
        concepto=F('idventa__concepto'),
        idtipomovimiento_id=Value(2)  # 2 para ventas
    ).values('fecha_movimiento', 'concepto', 'cantidad', 'preciounitario', 'valor', 'idtipomovimiento_id')

    # Obtener los lotes caducados que aún tienen cantidad
    '''lotes_caducados = Lotes.objects.filter(
        codigoarticulo__codigoarticulo=id_articulo,
        fecha_caducidad__lte=timezone.now().date(),  # Lotes caducados
        cantidad__gt=0  # Con cantidad mayor a 0
    ) 

    # Agregar salidas por caducidad como movimientos adicionales
    movimientos_caducidad = []
    for lote in lotes_caducados:
        detalle_compra_lote = Detalle_compra_lotes.objects.filter(idlote=lote).first()
        if detalle_compra_lote:
            movimientos_caducidad.append({
                'fecha_movimiento': lote.fecha_caducidad,
                'concepto': 'Salida por caducidad',
                'cantidad': lote.cantidad,
                'preciounitario': detalle_compra_lote.iddetalle_compra.preciounitario,
                'valor': round(lote.cantidad * detalle_compra_lote.iddetalle_compra.preciounitario, 2),
                'idtipomovimiento_id': 3  # 3 para salidas por caducidad
            })'''

    # Combinar las list(compras) + list(ventas) + movimientos_caducidad
    movimientos = list(compras) + list(ventas)

    # Ordenar los movimientos por fecha
    movimientos.sort(key=lambda x: (x['fecha_movimiento'], x['idtipomovimiento_id']))

    resultados = []

    if metodo == 'promedio_ponderado':
        saldo_anterior = Decimal('0.00')
        cantidad_existente = 0
        costo_ponderado = Decimal('0.00')
        saldo_v = Decimal('0.00')

        for movimiento in movimientos:
            if movimiento['idtipomovimiento_id'] == 1:  # Compras
                cantidad_existente += movimiento['cantidad']
                costo_ponderado += Decimal(movimiento['valor'])
                if cantidad_existente > 0:
                    saldo_anterior = (costo_ponderado / Decimal(cantidad_existente)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    saldo_v = saldo_anterior
                else:
                    costo_ponderado = Decimal('0.00')

            elif movimiento['idtipomovimiento_id'] == 2:  # Ventas
                cantidad_existente -= movimiento['cantidad']
                if cantidad_existente > 0:
                    costo_ponderado -= Decimal(movimiento['cantidad']) * saldo_v
                    saldo_anterior = (costo_ponderado / Decimal(cantidad_existente)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                else:
                    costo_ponderado = Decimal('0.00')

            elif movimiento['idtipomovimiento_id'] == 3:  # Salidas por caducidad
                cantidad_existente -= movimiento['cantidad']
                if cantidad_existente > 0:
                    costo_ponderado -= Decimal(movimiento['cantidad']) * saldo_v
                    saldo_anterior = (costo_ponderado / Decimal(cantidad_existente)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                else:
                    costo_ponderado = Decimal('0.00')

            # Redondear saldo_v a dos decimales
            saldo_v_redondeado = saldo_v.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # Agregar el resultado a la lista
            resultados.append({
                'fecha': movimiento['fecha_movimiento'],
                'detalle': movimiento['concepto'] if movimiento['concepto'] else ("Entrada" if movimiento['idtipomovimiento_id'] == 1 else "Salida"),
                'entradas': movimiento['cantidad'] if movimiento['idtipomovimiento_id'] == 1 else ' ',
                'vr_unitario_entradas': Decimal(movimiento['preciounitario']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if movimiento['idtipomovimiento_id'] == 1 and movimiento['cantidad'] != 0 else ' ',
                'vr_total_entradas': Decimal(movimiento['valor']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if movimiento['idtipomovimiento_id'] == 1 else ' ',
                'salidas': movimiento['cantidad'] if movimiento['idtipomovimiento_id'] in [2, 3] else ' ',
                'vr_unitario_salidas': saldo_v_redondeado if movimiento['idtipomovimiento_id'] in [2, 3] else ' ',
                'vr_total_salidas': (Decimal(movimiento['cantidad']) * saldo_v_redondeado).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if movimiento['idtipomovimiento_id'] in [2, 3] else ' ',
                'saldos': cantidad_existente or ' ',
                'vr_unitario_saldos': saldo_anterior if cantidad_existente != 0 else ' ',
                'total': costo_ponderado or ' '
            })

    elif metodo == 'peps':
        inventario = deque()  # Cola para manejar el inventario (PEPS)
        cantidad_existente = 0
        costo_total = 0

        for movimiento in movimientos:
            if movimiento['idtipomovimiento_id'] == 1:  # Compras
                # Agregar la compra al inventario
                inventario.append({
                    'cantidad': movimiento['cantidad'],
                    'preciounitario': movimiento['preciounitario'],
                    'valor': movimiento['valor']
                })
                cantidad_existente += movimiento['cantidad']
                costo_total += movimiento['valor']

            elif movimiento['idtipomovimiento_id'] == 2:  # Ventas
                cantidad_vendida = movimiento['cantidad']
                valor_total_salidas = 0

                while cantidad_vendida > 0 and inventario:
                    primer_lote = inventario[0]
                    if primer_lote['cantidad'] <= cantidad_vendida:
                        # Usar todo el lote
                        cantidad_vendida -= primer_lote['cantidad']
                        valor_total_salidas += primer_lote['valor']
                        inventario.popleft()
                    else:
                        # Usar parcialmente el lote
                        valor_total_salidas += cantidad_vendida * primer_lote['preciounitario']
                        primer_lote['cantidad'] -= cantidad_vendida
                        primer_lote['valor'] -= cantidad_vendida * primer_lote['preciounitario']
                        cantidad_vendida = 0

                cantidad_existente -= movimiento['cantidad']
                costo_total -= valor_total_salidas

            elif movimiento['idtipomovimiento_id'] == 3:  # Salidas por caducidad
                cantidad_vendida = movimiento['cantidad']
                valor_total_salidas = 0

                while cantidad_vendida > 0 and inventario:
                    primer_lote = inventario[0]
                    if primer_lote['cantidad'] <= cantidad_vendida:
                        # Usar todo el lote
                        cantidad_vendida -= primer_lote['cantidad']
                        valor_total_salidas += primer_lote['valor']
                        inventario.popleft()
                    else:
                        # Usar parcialmente el lote
                        valor_total_salidas += cantidad_vendida * primer_lote['preciounitario']
                        primer_lote['cantidad'] -= cantidad_vendida
                        primer_lote['valor'] -= cantidad_vendida * primer_lote['preciounitario']
                        cantidad_vendida = 0

                cantidad_existente -= movimiento['cantidad']
                costo_total -= valor_total_salidas

            # Calcular el saldo actual
            saldo_anterior = costo_total / cantidad_existente if cantidad_existente > 0 else 0

            # Agregar el resultado a la lista
            resultados.append({
                'fecha': movimiento['fecha_movimiento'],
                'detalle': movimiento['concepto'] if movimiento['concepto'] else ("Entrada" if movimiento['idtipomovimiento_id'] == 1 else "Salida"),
                'entradas': movimiento['cantidad'] if movimiento['idtipomovimiento_id'] == 1 else ' ',
                'vr_unitario_entradas': movimiento['preciounitario'] if movimiento['idtipomovimiento_id'] == 1 and movimiento['cantidad'] != 0 else ' ',
                'vr_total_entradas': movimiento['valor'] if movimiento['idtipomovimiento_id'] == 1 else ' ',
                'salidas': movimiento['cantidad'] if movimiento['idtipomovimiento_id'] in [2, 3] else ' ',
                'vr_unitario_salidas': primer_lote['preciounitario'] if movimiento['idtipomovimiento_id'] in [2, 3] else ' ',
                'vr_total_salidas': valor_total_salidas if movimiento['idtipomovimiento_id'] in [2, 3] else ' ',
                'saldos': cantidad_existente or ' ',
                'vr_unitario_saldos': round(saldo_anterior, 2) or ' ',
                'total': round(costo_total, 2) or ' '
            })

    return resultados


# Generar PDF Reporte Kardex
def generar_pdf_kardex(self, request):
    # Obtener valores
    empresa = Empresas.objects.get(idempresa=100)
    logo_url = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None # uso al no estar desplegado
    #logo_url = f"file://{os.path.join(settings.MEDIA_ROOT, empresa.logo.name)}" if empresa.logo else None # uso al estar desplegado
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Obtener valores request.GET
    articulo = Articulos.objects.get(codigoarticulo=request.GET.get('selectProducto'))
    metodo = request.GET.get('selectMetodo')
    fecha_kardex_desde = datetime.strptime(request.GET.get('fecha_kardex_desde', ''), '%Y-%m-%d').date()
    fecha_kardex_hasta = datetime.strptime(request.GET.get('fecha_kardex_hasta', ''), '%Y-%m-%d').date()
    kardex = kardex_articulo(articulo.codigoarticulo, metodo)

    # Filtrado in-place
    kardex_filtrado = []
    for kar in kardex:
        if (kar['fecha'] >= fecha_kardex_desde) and (kar['fecha'] <= fecha_kardex_hasta):
            kardex_filtrado.append(kar)

    # Pasar los valores al contexto
    context = {'empresa': empresa, 'kardex': kardex_filtrado, 'articulo_obj': articulo, 'metodo': request.GET.get('selectMetodo'), 'logo_url': logo_url, 'now': now,
        'fecha_kardex_desde': fecha_kardex_desde, 'fecha_kardex_hasta': fecha_kardex_hasta,
    }

    template_path = 'informe_pdf/kardex.html' # Renderizar el template HTML
    template = get_template(template_path)
    html = template.render(context)
    # Generar el pdf
    result = BytesIO()
    HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(result)
    return result.getvalue()


# Vista Genera PDF Reporte Kardex
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('empresa.generar_reportes', raise_exception=True), name='dispatch')
class GenerarPDFKardexView(View):
    def get(self, request, descargar, *args, **kwargs):
        pdf_content = generar_pdf_kardex(self, request)
        if pdf_content:
            filename = f"ReporteKardexProducto_{request.GET.get('selectProducto')}.pdf"  # Nombre del archivo PDF
            response = HttpResponse(pdf_content, content_type='application/pdf')
            if descargar == 'True':
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            else:
                response['Content-Disposition'] = f'filename="{filename}"'
            return response
        else:
            return HttpResponse("Error al generar el PDF.", status=500)

