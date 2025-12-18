from django.shortcuts import render, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.categorias.models import Categoriaarticulos
from apps.articulos.models import Articulos
from apps.categorias.forms import CategoriaForm
from django.contrib import messages

# Vista Lista de Categorias
@login_required
@permission_required('categorias.ver_categorias', raise_exception=True)
def listado_categorias(request):
    categorias=Categoriaarticulos.objects.all()
    return render(request, 'listado_categorias.html', {"categorias":categorias})

# Vista regristro de Categoria
@login_required
@permission_required('categorias.crear_categorias', raise_exception=True)
def registrar_categorias(request):
    form = CategoriaForm()
    if request.method=="POST":
        form=CategoriaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro de Categoría Exitoso!")
            return redirect("categorias:listado_categorias")
    
    return render(request, 'registrar_categorias.html', {"form": form})

# Vista Edición de Categoria
@login_required
@permission_required('categorias.editar_categorias', raise_exception=True)
def editar_categorias(request, pk_id):
    categoria = Categoriaarticulos.objects.get(idcategoriaarticulo=pk_id)
    form = CategoriaForm(instance=categoria)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        
        if form.is_valid():
            form.save()
            messages.success(request, "¡Categoría Modificada Correctamente!")
            return redirect("categorias:listado_categorias")
    
    return render(request, 'editar_categorias.html', {"form": form, 'pk':pk_id})

# Vista Eliminación de Categoria
@login_required
@permission_required('categorias.eliminar_categorias', raise_exception=True)
def eliminar_categorias(request, pk_id):
    categoria=Categoriaarticulos.objects.get(idcategoriaarticulo=pk_id)
    
    if Articulos.objects.filter(idcategoriaarticulo=categoria).exists():
        messages.error(request, "No se puede eliminar la categoría. Existen productos asociados a esta categoría.")
    else:
        categoria.delete()
        messages.success(request, "¡Categoría Eliminada Correctamente!")
    
    return redirect("categorias:listado_categorias")
