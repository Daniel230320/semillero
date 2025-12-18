from django.shortcuts import render, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.compras.models import Compras, Detalle_compras
from apps.articulos.models import Articulos
from apps.proveedores.models import Proveedores
from apps.lotes.models import Lotes, Detalle_compra_lotes
from django.contrib import messages
from datetime import datetime
from decimal import Decimal
import json
from django.urls import reverse

# Vista Registro de Compra
@login_required
@permission_required('compras.crear_compras', raise_exception=True)
def registrar_compras(request):
    # Obtener valores
    listar_articulos = Articulos.objects.filter(estado_articulo=1).order_by('stock', 'descripcion_articulo')
    lis_proveedores = Proveedores.objects.filter(estado_proveedor=1).order_by('idproveedor')
    contexto = {'lista_articulos':listar_articulos, 'lis_proveedores':lis_proveedores}

    # POST
    if request.method == 'POST':
        # Obtener datos de compra
        concepto_ = request.POST.get('comconcepto')
        proveedor = int(request.POST.get('proveedor'))
        fecha_entrada_ = datetime.strptime(request.POST.get('fecha_entrada'), '%Y-%m-%d')
        subtotal0_ = Decimal(request.POST.get('comsubtotal0'))
        subtotal12_ = Decimal(request.POST.get('comsubtotal12'))
        subtotal_ = Decimal(request.POST.get('comsubtotal'))
        valoriva_ = Decimal(request.POST.get('comvaloriva'))
        total_ = Decimal(request.POST.get('comtotal'))
        proveedor_obj = Proveedores.objects.get(idproveedor=proveedor) 

        # Obtener registro de detalles
        cantidades = request.POST.getlist('cantidad[]')
        valores = request.POST.getlist('valor[]')
        idarticulos = request.POST.getlist('idarticulo[]')
        preciounitarios = request.POST.getlist('precio_unitario[]')

        # Recibir y procesar los lotes (en formato JSON)
        lotes_json = request.POST.get('lotes')
        if lotes_json:
            lotes = json.loads(lotes_json)
        
        # Validar número de lote único
        '''if lotes:
            errores = []  # Lista para acumular mensajes de error
            for lote in lotes:
                if Lotes.objects.filter(numero_lote=lote['num_lote']).exists():
                    errores.append(f"El número de Lote '{lote['num_lote']}' ya existe para el producto '{Lotes.objects.get(numero_lote=lote['num_lote']).codigoarticulo}'.")
            if errores:
                messages.error(request, "<br>".join(errores))
                return render(request, 'registrar_compras.html', contexto)'''

        # Recopilar los productos que exceden el stock máximo
        
        # Crear y guardar Compra
        compra = Compras(
            user = request.user,
            concepto = concepto_,
            fecha_compra = fecha_entrada_,
            subtotal_tarifa0 = subtotal0_,
            subtotal_tarifa12 = subtotal12_,
            subtotal = subtotal_,
            valoriva = valoriva_,
            total = total_,
        )
        compra.idproveedor=proveedor_obj
        compra.save()
        compra = Compras.objects.get(idcompra=compra.idcompra)

        # Iterar sobre los detalles y guardar
        for cantidad_, valor_, idarticulo_, preciounitario_ in zip(cantidades, valores, idarticulos, preciounitarios):
            cantidad_ = int(cantidad_)
            valor_ = Decimal(valor_)
            idarticulo_ = int(idarticulo_)
            preciounitario_ = Decimal(preciounitario_)
            articulo = Articulos.objects.get(idarticulo=idarticulo_) # Obtener la instancia del artículo
            articulo.stock = articulo.stock + cantidad_
            articulo.save()

            # Crear y guardar el detalle asociado a la compra
            detalle = Detalle_compras(
                idcompra=compra, 
                codigoarticulo=articulo,
                cantidad=cantidad_,
                valor=valor_,
                preciounitario=preciounitario_,
            )
            detalle.save()

            # Guardar los lotes correspondientes
            if lotes:
                for lote in lotes:
                    if str(articulo.idarticulo) == lote['lote_articulo_id']:
                        nuevo_lote = Lotes(
                            numero_lote=lote['num_lote'],
                            cantidad=lote['cantidad_lote'],
                            fecha_fabricacion=(
                                datetime.strptime(lote['fecha_fabricacion'], "%Y-%m-%d").date() 
                                if lote['fecha_fabricacion'] else None
                            ),
                            fecha_caducidad=(
                                datetime.strptime(lote['fecha_caducidad'], "%Y-%m-%d").date() 
                                if lote['fecha_caducidad'] else None
                            ),
                            codigoarticulo=Articulos.objects.get(idarticulo=lote['lote_articulo_id']),  # Asociar al artículo correcto
                        )
                        nuevo_lote.save()

                        # Guardar el detalle de compra del lote
                        nuevo_detalle_compra_lote = Detalle_compra_lotes(
                            iddetalle_compra = detalle,
                            idlote = nuevo_lote,
                            cantidad = lote['cantidad_lote'],
                            valor = int(lote['cantidad_lote']) * preciounitario_
                        )
                        nuevo_detalle_compra_lote.save()

        messages.success(request, "¡Registro de Compra Exitoso!")
        return redirect('compras:registrar_compras')
    return render(request, 'registrar_compras.html', contexto)
