from django.shortcuts import render, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.proveedores.models import Proveedores
from apps.compras.models import Compras
from apps.proveedores.forms import ProveedorForm
from apps.proveedores.filters import ProveedoresFilter
from django.contrib import messages
from django.urls import reverse

# Vista lista de proveedores
@login_required
@permission_required('proveedores.ver_proveedores', raise_exception=True)
def listado_proveedores(request):
    proveedores=Proveedores.objects.all()
    filtro_proveedores = ProveedoresFilter(request.GET, queryset=proveedores)
    return render(request, 'listado_proveedores.html', {"proveedores": filtro_proveedores.qs, "filtro_proveedores": filtro_proveedores})

# Vista Registro de Proveedor
@login_required
@permission_required('proveedores.crear_proveedores', raise_exception=True)
def registrar_proveedores(request):
    form = ProveedorForm()
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro de Proveedor Exitoso!")
            if 'guardar_continuar' in request.POST:
                return redirect(reverse("proveedores:registrar_proveedores"))
            return redirect("proveedores:listado_proveedores")
        
        else:
            messages.error(request, "Error en el registro. Verifique los datos ingresados.")
    
    return render(request, 'registrar_proveedores.html', {"form": form})

# Vista Edición de Proveedor
@login_required
@permission_required('proveedores.editar_proveedores', raise_exception=True)
def editar_proveedores(request, pk_id):
    proveedor = Proveedores.objects.get(idproveedor=pk_id)
    form = ProveedorForm(instance=proveedor)
    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        
        if form.is_valid():
            form.save()
            messages.success(request, "¡Proveedor Modificado Correctamente!")
            if 'editar_continuar' in request.POST:
                return redirect(reverse("proveedores:editar_proveedores", args=[pk_id]))
            return redirect("proveedores:listado_proveedores")
        
        else:
            messages.error(request, "Error en la modificación. Verifique los datos ingresados.")
    
    return render(request, 'editar_proveedores.html', {"form": form})

# Vista Eliminación de Proveedor
@login_required
@permission_required('proveedores.eliminar_proveedores', raise_exception=True)
def eliminar_proveedores(request, pk_id):
    proveedor=Proveedores.objects.get(idproveedor=pk_id)
    if Compras.objects.filter(idproveedor=proveedor).exists():
        messages.error(request, "No se puede eliminar el proveedor. Está asociado a transacciones de compras.")
    else:
        proveedor.delete()
        messages.success(request, "¡Proveedor Eliminado Correctamente!")
    
    return redirect("proveedores:listado_proveedores")

# Vista Detalle de Proveedor
@login_required
@permission_required('proveedores.ver_proveedores', raise_exception=True)
def detalle_proveedor(request, pk_id):
    proveedor=Proveedores.objects.get(idproveedor=pk_id)
    return render(request, 'detalle_proveedor.html', {"proveedor": proveedor})