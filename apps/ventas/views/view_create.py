from django.shortcuts import render, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.ventas.models import Ventas, Detalle_ventas, Pagos, Formapagos
from apps.articulos.models import Articulos
from apps.lotes.models import Lotes, Estado_lotes
from apps.clientes.models import Clientes
from django.contrib import messages
from datetime import datetime
from decimal import Decimal

# Vista Registro de Venta
@login_required
@permission_required('ventas.crear_ventas', raise_exception=True)
def registrar_ventas(request):
    # Obtener valores
    listar_articulos=Articulos.objects.filter(estado_articulo=1).order_by('descripcion_articulo')
    lis_clientes=Clientes.objects.filter(estado_cliente=1).order_by('idcliente')
    contexto={'listar_articulos':listar_articulos, 'lis_clientes':lis_clientes}

    # POST
    if request.method == 'POST':
        concepto_ = request.POST.get('concepto')
        # Validar q no se pase el stock
        errores = []
        for can, idar in zip(request.POST.getlist('cantidad[]'), request.POST.getlist('idarticulo[]')):
            articulo = Articulos.objects.get(idarticulo=int(idar))
            if articulo.stock < int(can):
                errores.append(f"1. El producto '{articulo}' no tiene suficiente stock disponible.")
        if errores:
            messages.error(request, "<br>".join(errores))
            return render(request, 'ventas/registrar_ventas.html', contexto)
        
        # Obtener datos de venta
        cliente = int(request.POST.get('cliente'))
        fecha_emision_ = datetime.strptime(request.POST.get('fecha_emision'), '%Y-%m-%d')
        subtotal0_ = Decimal(request.POST.get('subtotal0'))
        subtotal12_ = Decimal(request.POST.get('subtotal12'))
        subtotal_ = Decimal(request.POST.get('subtotal'))
        valoriva_ = Decimal(request.POST.get('valoriva'))
        total_ = Decimal(request.POST.get('total'))
        descuentototal_ = Decimal(request.POST.get('descuentototal'))
        cliente_obj = Clientes.objects.get(idcliente=cliente)

        # Crear y guardar venta
        venta = Ventas(
            user = request.user,
            concepto = concepto_,
            fecha_venta = fecha_emision_,
            subtotal_tarifa0 = subtotal0_,
            subtotal_tarifa12 = subtotal12_,
            subtotal = subtotal_,
            valoriva = valoriva_,
            total = total_,
            descuento = descuentototal_,
        )
        venta.idcliente=cliente_obj
        venta.save()

        # Obtener registro de detalles
        descuentototales =request.POST.getlist('descuentoProdu[]')
        cantidades = request.POST.getlist('cantidad[]')
        valores = request.POST.getlist('valor[]')
        idarticulos = request.POST.getlist('idarticulo[]')
        preciounitarios = request.POST.getlist('precio_unitario[]')
        venta = Ventas.objects.get(idventa=venta.idventa)

        # Iterar sobre los detalles y guárdalos
        for descuentoto_, cantidad_, valor_, idarticulo_, preciounitario_ in zip(descuentototales, cantidades, valores, idarticulos, preciounitarios):
            descuentoto_ = Decimal(descuentoto_)
            cantidad_ = int(cantidad_)
            valor_ = Decimal(valor_)
            idarticulo_ = int(idarticulo_)
            preciounitario_ = Decimal(preciounitario_)
            articulo = Articulos.objects.get(idarticulo=idarticulo_) # Obtener la instancia del artículo
            articulo.stock = articulo.stock - cantidad_
            articulo.save()

            # Crear y guardar el detalle asociado a la venta
            detalle = Detalle_ventas(
                idventa=venta, 
                codigoarticulo=articulo,
                cantidad=cantidad_,
                valor=valor_,
                valordescuento=descuentoto_,
                preciounitario=preciounitario_,
            )
            # productos que tienen lote restar stock
            lotes = Lotes.objects.exclude(idestado_lote=Estado_lotes.objects.get(code_estado_lote='vencido')).filter(codigoarticulo=articulo, cantidad__gt=0).order_by('fecha_caducidad')
            cantidad_restante = cantidad_  # Cantidad que aún se debe descontar
            for lote in lotes:
                '''if lote.fecha_caducidad is not None and lote.fecha_caducidad <= date.today() and not lote.idestado_lote.code_estado_lote == 'vencido':
                    lote.idestado_lote = Estado_lotes.objects.get(code_estado_lote='vencido')
                    articulo.stock -= lote.cantidad
                    lote.save()
                    articulo.save()
                    continue'''
                if cantidad_restante <= 0:
                    break 
                if lote.cantidad >= cantidad_restante:
                    lote.cantidad -= cantidad_restante
                    cantidad_restante = 0
                else:
                    cantidad_restante -= lote.cantidad 
                    lote.cantidad = 0 
                lote.save()
            detalle.save()

        # Crear y guardar pago
        pago = Pagos( # Opcional de pagos
            idventa=venta,
            idformapago=Formapagos.objects.get(idformapago=1),
            monto = Decimal(request.POST.get('efectivo_recibido')),
        )
        pago.save()

        messages.success(request, "¡Registro de Venta Exitoso!")
        #return redirect('ventas:listado_ventas')
        contexto['id_factura']=venta.idventa
        #return render(request, 'ventas/registrar_ventas.html', contexto)
    return render(request, 'ventas/registrar_ventas.html', contexto)
