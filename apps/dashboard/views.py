from django.shortcuts import render, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from datetime import date
from decimal import Decimal
import json
from apps.ventas.models import Ventas, Detalle_ventas
from apps.articulos.models import Articulos
from apps.clientes.models import Clientes
from apps.proveedores.models import Proveedores
from apps.compras.models import Compras
from apps.usuarios.models import CustomUser

# Vista del Dashboard (inicio)
@login_required
def inicio(request):
    # Otener fecha actual
    fecha_actual = date.today()
    mes_actual = fecha_actual.month
    año_actual = fecha_actual.year

    # Obtener ganancias mensuales y pasar a JSON
    ganancias_mensuales = []
    for mes in range(1, 13):
        ventas_mes = (
            Ventas.objects
            .filter(fecha_venta__year=año_actual, fecha_venta__month=mes)
            .aggregate(total_ventas=Sum('total'))
        )
        ganancias_mes = ventas_mes['total_ventas'] or Decimal('0')
        ganancias_mensuales.append(float(ganancias_mes))
    ganancias_mensuales_json = json.dumps(ganancias_mensuales)

    # Obtener totales
    total_existencia_vendida = Detalle_ventas.objects.aggregate(total=Sum('cantidad'))['total'] or 0
    total_existencia_actual = Articulos.objects.aggregate(total=Sum('stock'))['total'] or 0
    existencia_total = total_existencia_vendida + total_existencia_actual
    
    # Calcular ganancias
    ganancias_anual = (
        Ventas.objects
        .filter(fecha_venta__year=año_actual)
        .aggregate(total_anual=Sum('total'))
        ['total_anual'] or 0
    )  
    ganancias_mensual = (
        Ventas.objects
        .filter(fecha_venta__year=año_actual, fecha_venta__month=mes_actual)
        .aggregate(total_mensual=Sum('total'))
        ['total_mensual'] or 0
    )
    
    # Resultados de ventas
    res_ultima10_ventas = Ventas.objects.order_by('-fecha_venta')[:10]
    articulos_mas_vendidos = (
        Detalle_ventas.objects
        .filter(idventa__fecha_venta__year=año_actual)
        .values('codigoarticulo__descripcion_articulo', 'preciounitario',)
        .annotate(cantidad_vendida=Sum('cantidad'), total_vendido=Sum(F('cantidad') * F('preciounitario')))
        .order_by('-total_vendido')[:10]
    )
    articulos_vendidos_json = json.dumps([
        {
            'descripcion': item['codigoarticulo__descripcion_articulo'],
            'precio': float(item['preciounitario']), 
            'cantidad_vendida': int(item['cantidad_vendida']),
            'total_vendido': float(item['total_vendido']),
        }
        for item in articulos_mas_vendidos
    ])
    
    # Renderizar la plantilla
    contexto = {
        'total_clientes': Clientes.objects.count(), 'total_proveedores': Proveedores.objects.count(),
        'total_articulos': Articulos.objects.count(), 'total_compras': Compras.objects.count(),
        'total_ventas': Ventas.objects.count(), 'total_usuarios': CustomUser.objects.count(),
        'total_existencia_vendida': total_existencia_vendida, 'total_existencia_actual': total_existencia_actual,
        'total_existencia_total': existencia_total, 'ganancias_m': ganancias_mensual,
        'ganancias_anual': ganancias_anual,'resumen_ganancias': ganancias_mensuales_json,
        'articulos_vendidos': articulos_vendidos_json, 'ultima10_ventas': res_ultima10_ventas,
    }
    return render(request, 'inicio.html', contexto)
