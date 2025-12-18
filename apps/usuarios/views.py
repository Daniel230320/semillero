from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from apps.usuarios.models import CustomUser
from apps.ventas.models import Ventas
from apps.compras.models import Compras
from apps.usuarios.filters import CustomUserFilter
from apps.usuarios.forms import *
from django.contrib import messages
from django.urls import reverse

# Vista perfil de usuario
@login_required
def cuenta_perfil(request):
    # Recibir datos
    if request.method == 'POST':
        # Actualizar información
        if 'update_info' in request.POST:
            user_form = CustomUserChangeForm(request.POST, instance=request.user)
            password_form = CustomPasswordChangeForm(request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Información actualizada con éxito.')
                return redirect('usuarios:cuenta_perfil')
            else:
                messages.error(request, 'Errores en el formulario de información.')
        
        # Actualizar contraseña
        elif 'change_password' in request.POST:
            user_form = CustomUserChangeForm(instance=request.user)
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Contraseña actualizada con éxito.')
                return redirect('usuarios:cuenta_perfil')
            else:
                messages.error(request, 'Errores en el formulario de cambio de contraseña.')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'profile/cuenta_perfil.html', {'user_form': user_form, 'password_form': password_form,})

# Vista Lista de Usuarios
@login_required
@permission_required('usuarios.ver_usuarios', raise_exception=True)
def listado_usuarios(request):
    usuarios = CustomUser.objects.exclude(username=request.user.username).exclude(is_superuser=True)
    user_filter = CustomUserFilter(request.GET, queryset=usuarios)
    return render(request, 'usuarios/listado_usuarios.html', {'usuarios': user_filter.qs, 'filter': user_filter})

# Vista Registro de Usuario
@login_required
@permission_required('usuarios.crear_usuarios', raise_exception=True)
def registrar_usuarios(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            grupo_seleccionado = form.cleaned_data.get('groups')
            
            if grupo_seleccionado:
                user.groups.set([grupo_seleccionado])
            messages.success(request, "¡Registro de Usuario Exitoso!")
            if 'guardar_continuar' in request.POST:
                return redirect(reverse("usuarios:registrar_usuarios"))
            return redirect('usuarios:listado_usuarios')
        
        else:
            messages.error(request, "Error en el registro. Verifique los datos ingresados.")
    
    return render(request, 'usuarios/registrar_usuarios.html', {"form": form})

# Vista Edición de Usuario
@login_required
@permission_required('usuarios.editar_usuarios', raise_exception=True)
def editar_usuarios(request, pk_id):
    usuario = get_object_or_404(CustomUser, pk=pk_id)
    form = CustomUserEditionForm(instance=usuario)
    password_form = CustomUserEditionPasswordForm()
    
    # Recibir datos
    if request.method == 'POST':
        # Actualizar información
        if 'user_update_info' in request.POST:
            form = CustomUserEditionForm(request.POST, instance=usuario)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                grupos_seleccionado = form.cleaned_data.get('groups')
                if grupos_seleccionado:
                    user.groups.set([grupos_seleccionado])
                messages.success(request, "¡Información general del usuario modificada correctamente!")
                if 'editar_continuar' in request.POST:
                    return redirect(reverse("usuarios:editar_usuarios", args=[pk_id]))
                return redirect('usuarios:listado_usuarios')
            else:
                messages.error(request, "Error en la modificación. Verifique los datos ingresados.")
        
        # Actualizar contraseña
        elif 'user_change_password' in request.POST:
            password_form = CustomUserEditionPasswordForm(request.POST)
            if password_form.is_valid():
                usuario.set_password(password_form.cleaned_data['password1'])  # Se actualiza la contraseña
                usuario.save()
                messages.success(request, 'Contraseña del usuario actualizada con éxito.')
                return redirect('usuarios:listado_usuarios')
            else:
                messages.error(request, 'Errores en el formulario de cambio de contraseña.')
    
    return render(request, 'usuarios/editar_usuarios.html', {'form': form, 'user_password_form': password_form,})

# Vista Eliminación de Usuario
@login_required
@permission_required('usuarios.eliminar_usuarios', raise_exception=True)
def eliminar_usuarios(request, pk_id):
    usuario = CustomUser.objects.get(pk=pk_id)
    existe_compras = Compras.objects.filter(user=usuario).exists()
    existe_ventas = Ventas.objects.filter(user=usuario).exists()
    
    if existe_compras or existe_ventas:
        messages.error(request, "No se puede eliminar el usuario. Está asociado a transacciones de compras o ventas.")
    else:
        usuario.delete()
        messages.success(request, "¡Usuario Eliminado Correctamente!")
    
    return redirect('usuarios:listado_usuarios')

# Vista Detalle de Usuario
@login_required
@permission_required('usuarios.ver_usuarios', raise_exception=True)
def detalle_usuario(request, pk_id):
    usuario = CustomUser.objects.get(id=pk_id)
    roles_usuario = usuario.groups.filter()
    return render(request, 'usuarios/detalle_usuario.html', {"usuario": usuario, "roles_usuario": roles_usuario})
