from django.shortcuts import render, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.clientes.models import Clientes
from apps.ventas.models import Ventas
from apps.clientes.forms import ClienteForm
from apps.clientes.filters import ClientesFilter
from django.contrib import messages
from django.urls import reverse

# Vista lista de clientes
@login_required
@permission_required('clientes.ver_clientes', raise_exception=True)
def listado_clientes(request):
    clientes = Clientes.objects.all()
    filtro_clientes = ClientesFilter(request.GET, queryset=clientes)
    return render(request, 'listado_clientes.html', {"clientes": filtro_clientes.qs, "filtro_clientes": filtro_clientes})

# Vista Registro de Cliente
@login_required
@permission_required('clientes.crear_clientes', raise_exception=True)
def registrar_clientes(request):
    form = ClienteForm()
    if request.method == "POST":
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro de Cliente Exitoso!")
            if 'guardar_continuar' in request.POST: 
                return redirect(reverse("clientes:registrar_clientes"))
            return redirect("clientes:listado_clientes")
        
        else:
            messages.error(request, "Error en el registro. Verifique los datos ingresados.")
    
    return render(request, 'registrar_clientes.html', {"form": form})

# Vista Edición de Cliente
@login_required
@permission_required('clientes.editar_clientes', raise_exception=True)
def editar_clientes(request, pk_id):
    cliente = Clientes.objects.get(idcliente=pk_id)
    form = ClienteForm(instance=cliente)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        
        if form.is_valid():
            form.save()
            messages.success(request, "¡Cliente Modificado Correctamente!")
            if 'editar_continuar' in request.POST: 
                return redirect(reverse("clientes:editar_clientes", args=[pk_id]))
            return redirect("clientes:listado_clientes")
        
        else:
            messages.error(request, "Error en la modificación. Verifique los datos ingresados.")
    
    return render(request, 'editar_clientes.html', {"form": form})

# Vista Eliminación de Cliente
@login_required
@permission_required('clientes.eliminar_clientes', raise_exception=True)
def eliminar_clientes(request, pk_id):
    cliente=Clientes.objects.get(idcliente=pk_id)
    
    if Ventas.objects.filter(idcliente=cliente).exists():
        messages.error(request, "No se puede eliminar el cliente. Está asociado a transacciones de ventas.")
    else:
        cliente.delete()
        messages.success(request, "¡Cliente Eliminado Correctamente!")
    
    return redirect("clientes:listado_clientes")

# Vista Detalle de Cliente
@login_required
@permission_required('clientes.ver_clientes', raise_exception=True)
def detalle_cliente(request, pk_id):
    cliente=Clientes.objects.get(idcliente=pk_id)
    return render(request, 'detalle_cliente.html', {"cliente": cliente})
