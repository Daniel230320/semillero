from django.shortcuts import render, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.lotes.models import Lotes
from apps.lotes.forms import LotesForm
from apps.lotes.filters import LoteFilter
from django.contrib import messages
from django.utils import timezone

# Vista lista de lotes
@login_required
@permission_required('lotes.ver_lotes', raise_exception=True)
def listado_lotes(request):
    # Obtener los lotes
    lotes = Lotes.objects.none()
    filtro_lotes = LoteFilter(request.GET, queryset=Lotes.objects.all())
    lotes = filtro_lotes.qs
    
    # Agregar días disponibles a cada lote
    for lot in lotes:
        if lot.fecha_caducidad:
            lot.dias_disponibles = (lot.fecha_caducidad - timezone.now().date()).days
        else:
            lot.dias_disponibles = None
    
    return render(request, 'listado_lotes.html', {"lotes": lotes, "filtro_lotes": filtro_lotes})

# Vista Edición de Lote
@login_required
@permission_required('lotes.editar_lotes', raise_exception=True)
def editar_lotes(request, pk_id):
    lote = Lotes.objects.get(idlote=pk_id)
    form = LotesForm(instance=lote)
    if request.method=="POST":
        form = LotesForm(request.POST, instance=lote)
        form.save()
        messages.success(request, "¡Lote Modificado Correctamente!")
        return redirect("lotes:listado_lotes")
    
    return render(request, 'editar_lotes.html', {"form":form, 'lote':lote})