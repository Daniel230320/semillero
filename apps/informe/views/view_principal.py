from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from apps.articulos.models import Articulos
from django.http import JsonResponse

# Vista Principal
@login_required
@permission_required('empresa.generar_reportes', raise_exception=True)
def reporte_inicio(request):
    return render(request, 'informe_principal/informe_inicio.html')

# Vista AJAX productos por categoria
def get_productos_por_categoria(request):
    categoria_id = request.GET.get('categoria_id')
    productos = Articulos.objects.all().values('idarticulo', 'descripcion_articulo')
    if categoria_id:
        productos = productos.filter(idcategoriaarticulo=categoria_id)
    return JsonResponse(list(productos), safe=False)

# Vista AJAX productos caducos por categoria
def get_caducos_por_categoria(request):
    categoria_id = request.GET.get('categoria_id')
    productos = Articulos.objects.all().values('idarticulo', 'descripcion_articulo')
    if categoria_id:
        productos = productos.filter(idcategoriaarticulo=categoria_id, tiene_fecha_caduca=True)
        print(productos)
    return JsonResponse(list(productos), safe=False)
