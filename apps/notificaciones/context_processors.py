# Context_processors
from apps.notificaciones.models import NotificationCustomUser
from django.utils.timezone import now

# Vista de conexto de notificaciones
def notificaciones(request):
    # Obtener las notificaciones del usuario
    total_notificaciones = NotificationCustomUser.objects.none()
    notificaciones_base = NotificationCustomUser.objects.none()
    nuevas_notificaciones = NotificationCustomUser.objects.none()

    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        total_notificaciones = NotificationCustomUser.objects.filter(user=request.user, read=False).count()
        notificaciones_base = NotificationCustomUser.objects.filter(user=request.user, read=False)
        if notificaciones_base.exists():
            diferencia = (now() - notificaciones_base.first().created).total_seconds()
            if diferencia <= 5: nuevas_notificaciones = True # Si fue creada hace 5s

    # Retornar el contexto
    return {
        'total_notificaciones': total_notificaciones,
        'notificaciones_base': notificaciones_base,
        'nuevas_notificaciones': nuevas_notificaciones,
    }