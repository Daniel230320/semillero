from django.shortcuts import render, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from apps.roles.forms import GroupForm, PermisoForm
from django.contrib import messages
from django.contrib.auth.models import Group

# Vista lista de Roles
@login_required
@permission_required('usuarios.ver_roles', raise_exception=True)
def roles(request):
    roles = Group.objects.all().order_by('name')
    return render(request, 'roles.html', {"roles": roles})

# Vista Eliminación de Rol
@login_required
@permission_required('usuarios.eliminar_roles', raise_exception=True)
def eliminar_roles(request, pk_id):
    Group.objects.get(pk=pk_id).delete()
    messages.success(request, "¡Rol Eliminado Correctamente!")
    return redirect('roles:roles')

# Vista Registro de Rol
@login_required
@permission_required('usuarios.crear_roles', raise_exception=True)
def registrar_roles(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro de Rol Exitoso!")
            return redirect('roles:roles')
    
    return render(request, 'registrar_roles.html', {'form': form})

# Vista Edición de Rol
@login_required
@permission_required('usuarios.editar_roles', raise_exception=True)
def editar_roles(request, pk_id):
    rol = Group.objects.get(pk=pk_id)
    form = GroupForm(instance=rol)
    if request.method=="POST":
        form = GroupForm(request.POST, instance=rol)
        form.save()
        messages.success(request, "¡Rol Modificado Correctamente!")
        return redirect("roles:roles")
    
    return render(request, 'editar_roles.html', {"form":form, 'pk':pk_id})

# Vista Asignación de Permisos a Rol
@login_required
@permission_required('usuarios.asignar_permisos_roles', raise_exception=True)
def permiso_roles(request, pk_id):
    permiso_grupo = Group.objects.get(pk=pk_id)
    form = PermisoForm(instance=permiso_grupo)
    if request.method == "POST":
        form = PermisoForm(request.POST, instance=permiso_grupo)
        
        if form.is_valid():
            form.save()
            
            # Asignar permisos directamente al usuario
            for usuario in permiso_grupo.user_set.all():
                usuario.user_permissions.set(form.cleaned_data['permissions'])
            messages.success(request, "¡Permisos del Rol Modificados Correctamente!")
            return redirect("roles:roles")
    
    return render(request, 'permiso_roles.html', {"form": form, 'pk': pk_id})
