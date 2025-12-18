# lotes/tasks.py
from celery import shared_task
from django.utils import timezone
from apps.articulos.models import Articulos
from apps.usuarios.models import CustomUser
from apps.notificaciones.models import Notification, NotificationCustomUser
from apps.lotes.models import Lotes, Estado_lotes
from apps.empresa.models import Empresas
from django.contrib.contenttypes.models import ContentType

def enviar_notificacion_caducidad(lote):
    """ Verificar el estado de los lotes y enviar notificaciones """
    content_type = ContentType.objects.get_for_model(Articulos)
    mensaje_general = f"El producto '{lote.codigoarticulo}' con código: {lote.codigoarticulo.codigoarticulo}, su lote '{lote.numero_lote}' con fecha de caducidad del {lote.fecha_caducidad.strftime('%d/%m/%Y')}"
    if lote.idestado_lote.code_estado_lote == 'por_vencer':
        dias_restantes = (lote.fecha_caducidad - timezone.now().date()).days
        mensaje = f"{mensaje_general}, está próximo a vencer en {dias_restantes} días."
        notificacion_id = 4
    elif lote.idestado_lote.code_estado_lote == 'vencido':
        mensaje = f"{mensaje_general}, se encuentra vencido."
        notificacion_id = 5
    else:
        return
    
    # Crear notificación para cada usuario
    usuarios = CustomUser.objects.all()
    if Empresas.objects.get(idempresa=100).notificar_a == 'superuser':
        usuarios = CustomUser.objects.filter(is_superuser=True)
    for user in usuarios:
        NotificationCustomUser.objects.create(
            idnotification=Notification.objects.get(idnotification=notificacion_id),
            user=user,
            message=mensaje,
            target_content_type=content_type,
            target_id=lote.codigoarticulo.idarticulo,
            target_object=lote.codigoarticulo
        )

@shared_task
def verificar_estado_lotes():
    """Verificar fecha de caducidad de los lotes y enviar notificaciones"""
    lotes = Lotes.objects.all()
    for lote in lotes:
        # Si no hay fecha de caducidad
        if not lote.fecha_caducidad:
            lote.idestado_lote = Estado_lotes.objects.get(code_estado_lote='no_vence')
        
        # Por el contrario
        else:
            dias_restantes = (lote.fecha_caducidad - timezone.now().date()).days
            dias_por_vencer = Empresas.objects.get(idempresa=100).dias_por_vencer_general or 5
            
            # Vencido si quedan menos de 0 días y estado 'vencido'
            if dias_restantes <= 0 and not lote.idestado_lote.code_estado_lote == 'vencido':
                lote.idestado_lote = Estado_lotes.objects.get(code_estado_lote='vencido')
                articulo = Articulos.objects.get(idarticulo=lote.codigoarticulo.idarticulo)
                articulo.stock -= lote.cantidad
                articulo.save()
                if lote.cantidad > 0:
                    enviar_notificacion_caducidad(lote)
            
            # Por vencer si quedan dias_por_vencer días o menos
            elif dias_restantes > 0 and dias_restantes <= dias_por_vencer:
                lote.idestado_lote = Estado_lotes.objects.get(code_estado_lote='por_vencer')
                if lote.cantidad > 0:
                    enviar_notificacion_caducidad(lote)
            
            # Vigente si quedan más de dias_por_vencer días
            elif dias_restantes > dias_por_vencer:
                lote.idestado_lote = Estado_lotes.objects.get(code_estado_lote='vigente')
        
        # Si la cantidad es 0, se considera como consumido
        if lote.cantidad == 0:
            lote.idestado_lote = Estado_lotes.objects.get(code_estado_lote='consumido')
        
        # Guardar cambios
        lote.save()
        