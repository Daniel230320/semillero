from django.shortcuts import render, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.empresa.models import Empresas, Ciudades
from apps.empresa.forms import EmpresaForm
from apps.articulos.models import Givas
from apps.articulos.forms import GivasForm
from django.contrib import messages
from django.http import JsonResponse
from django.forms import modelformset_factory

@login_required
@permission_required('empresa.editar_empresa', raise_exception=True)
def configuracion(request):
    GivasFormSet = modelformset_factory(Givas, form=GivasForm, extra=0)
    givas = Givas.objects.all().order_by('idgiva')[:2]
    giva_formset = GivasFormSet(queryset=givas)

    empresa = Empresas.objects.get(idempresa=100)
    empresa_form = EmpresaForm(instance=empresa)

    if request.method == "POST":
        giva_formset = GivasFormSet(request.POST, queryset=givas)
        empresa_form = EmpresaForm(request.POST, request.FILES, instance=empresa)

        if giva_formset.is_valid() and empresa_form.is_valid():
            giva_formset.save()
            empresa_form.save()
            messages.success(request, "¡Configuraciones del sistema actualizadas correctamente!")
            return redirect("empresa:configuracion")
        else:
            messages.error(request, "¡Error al guardar los datos, verifique los datos ingresados!")
    return render(request, 'configuracion.html', {"form": empresa_form, "empresa": empresa, "formset": giva_formset})

# AJAX
def ciudades_por_provincia(request, provincia_id):
    ciudades = Ciudades.objects.filter(idprovincia=provincia_id).values('pk', 'nombre_ciudad').order_by('nombre_ciudad')
    return JsonResponse({'ciudades': list(ciudades)})
