from django.db import models
from apps.usuarios.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.timesince import timesince

# Clase Nivel de Notificación
class Level(models.Model):
    idlevel = models.AutoField(primary_key=True)
    level_name = models.CharField(max_length=30, verbose_name="Nombre")

    def __str__(self):
        return self.level_name
    
    class Meta:
        db_table="levels"
        verbose_name="Nivel"
        verbose_name_plural="Niveles"

# Clase Notificación
class Notification(models.Model):
    idnotification = models.AutoField(primary_key=True)
    idlevel = models.ForeignKey(Level, on_delete=models.RESTRICT, verbose_name="Nivel")
    verb = models.CharField(max_length=30, verbose_name="Verbo")
    description = models.CharField(max_length=80, verbose_name="Descripción")
    public = models.BooleanField(default=True, verbose_name="Público")
    deleted = models.BooleanField(default=False, verbose_name="Eliminado")
    emailed = models.BooleanField(default=False, verbose_name="Enviado por correo")

    def __str__(self):
        return self.description
    
    class Meta:
        db_table="notifications"
        verbose_name="Notificación"
        verbose_name_plural="Notificaciones"
# Agregar limite de tiempo para eliminar notificaciones

# Clase Notificación de Usuario
class NotificationCustomUser(models.Model):
    idnotification = models.ForeignKey(Notification, on_delete=models.RESTRICT, verbose_name="Notificación")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Usuario")
    message = models.CharField(max_length=400, verbose_name="Mensaje")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    read = models.BooleanField(default=False, verbose_name="Leído")
    # Para manejar las entidades genéricas (tipo e ID)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.RESTRICT, verbose_name="Tipo de Entidad Objetivo")
    target_id = models.PositiveIntegerField(verbose_name="ID de Entidad Objetivo")
    target_object = GenericForeignKey('target_content_type', 'target_id')

    # Obtener el tiempo transcurrido desde la creación
    def elapsed_time(self):
        return timesince(self.created)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-created']
        db_table = "notifications_auth_user"
        verbose_name = "Notificación de Usuario"
        verbose_name_plural = "Notificaciones de Usuarios"

        