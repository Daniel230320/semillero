from django.shortcuts import render, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.compras.models import Compras, Detalle_compras

# Vista Edición de Compra
@login_required
@permission_required('compras.ver_compras', raise_exception=True)
def detalle_compras(request, pk_id):
    # Obtener datos
    detalles_compra = Detalle_compras.objects.filter(idcompra=pk_id)
    compra = Compras.objects.get(idcompra=pk_id)

    # Renderizar plantilla
    contexto = {
        "compra": compra, 
        "result_detalles": detalles_compra
    }
    return render(request, 'detalle_compras.html', contexto)
