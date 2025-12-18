from django.shortcuts import render, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.compras.models import Compras
from apps.compras.filters import ComprasFilter

# Vista lista de compras
@login_required
@permission_required('compras.ver_compras', raise_exception=True)
def listado_compras(request):
    # Obtener datos
    compras = Compras.objects.all().filter(user=request.user)
    if request.user.is_superuser:
        compras = Compras.objects.all()
    filtro = ComprasFilter(request.GET, queryset=compras)
    
    # Renderizar plantilla
    contexto = {"compras": filtro.qs, "filtro": filtro,}
    return render(request, 'listado_compras.html', contexto)
