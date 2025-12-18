from django.shortcuts import render, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.ventas.models import Ventas
from apps.ventas.filters import VentasFilter

# Vista Lista de Ventas
@login_required
@permission_required('ventas.ver_ventas', raise_exception=True)
def listado_ventas(request):
    # Obtener datos
    ventas = Ventas.objects.all().filter(user=request.user)
    if request.user.is_superuser:
        ventas = Ventas.objects.all()
    filtro = VentasFilter(request.GET, queryset=ventas)

    # Renderizar plantilla
    contexto = {"ventas": filtro.qs, "filtro": filtro}
    return render(request, 'ventas/listado_ventas.html', contexto)

