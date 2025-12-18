from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.notificaciones.models import NotificationCustomUser
from apps.notificaciones.filters import NotificationCustomUserFilter
from django.contrib import messages

# Vista notificaciones
@login_required
def notifications(request):
    notificaciones = NotificationCustomUser.objects.filter(user=request.user)
    filter = NotificationCustomUserFilter(request.GET, queryset=notificaciones)
    if request.method == "POST":
        seleccionadas = request.POST.getlist('notificaciones_seleccionadas')
        accion = request.POST.get('accion')
        
        if seleccionadas:
            notificaciones = NotificationCustomUser.objects.filter(id__in=seleccionadas, user=request.user)
            
            if accion == "eliminar":
                notificaciones.delete()
                messages.success(request, "¡Notificación(es) Eliminada(s) Correctamente!")
            
            elif accion == "marcar_leidas":
                notificaciones.update(read=True)
                messages.success(request, "¡Notificación(es) marcadas como leída(s) correctamente!")
        
        else: messages.error(request, "¡Seleccione al menos una Notificación!")
    
    return render(request, 'notifications.html', {'notificaciones': filter.qs, 'filter':filter})

# Vista notificaciones marcar como leídas
@login_required
def notifications_mark_as_read(request):
    notificaciones = NotificationCustomUser.objects.filter(user=request.user, read=False)
    if notificaciones.exists():
        notificaciones.update(read=True)
        messages.success(request, "¡Notificación(es) marcadas como leída(s) correctamente!")
    else:
        messages.error(request, "¡No hay Notificaciones Nuevas!")
    
    return redirect('notificaciones:notifications')

# Vista notificaciones eliminar todas
@login_required
def notifications_delete_all(request):
    notificaciones = NotificationCustomUser.objects.filter(user=request.user, read=False)
    if notificaciones.exists():
        notificaciones.delete()
        messages.success(request, "¡Notificación(es) sin leer Eliminada(s) Correctamente!")
    else:
        messages.error(request, "¡No hay Notificaciones sin leer para eliminar!")
    
    return redirect('notificaciones:notifications')

# Vista detalle notificación
@login_required
def detalle_notificacion(request, pk_id):
    notificacion = get_object_or_404(NotificationCustomUser, pk=pk_id, user=request.user)
    return render(request, 'detalle_notificacion.html', {'notificacion': notificacion})
