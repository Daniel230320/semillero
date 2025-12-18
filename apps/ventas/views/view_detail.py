from django.shortcuts import render, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.ventas.models import Ventas, Detalle_ventas, Pagos

# Vista Detalle de Venta
@login_required
@permission_required('ventas.ver_ventas', raise_exception=True)
def detalle_ventas(request, pk_id):
    # Obtener datos
    detalles_venta = Detalle_ventas.objects.filter(idventa=pk_id)
    venta = Ventas.objects.get(idventa=pk_id)
    pago = Pagos.objects.get(idventa=pk_id) # opcional de pagos
    
    # Renderizar plantilla
    contexto = {
        "venta": venta, 
        "result_detalles": detalles_venta, 
        "pago": pago, 
        "cambio": pago.monto-venta.total
    }
    return render(request, 'ventas/detalle_ventas.html', contexto)
