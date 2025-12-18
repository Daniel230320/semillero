# celery.py
import os
from celery import Celery
from django.conf import settings

# Establecer la variable de entorno para el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoDjango.settings')

# Crear instancia de Celery
app = Celery('proyectoDjango')

# Configurar Celery usando la configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Registra las tareas automáticamente desde las aplicaciones
app.autodiscover_tasks(['apps.notificaciones'])