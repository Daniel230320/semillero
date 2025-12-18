"""
WSGI config for proyectoDjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoDjango.settings')

application = get_wsgi_application()

# DESPLIEGUE RENDER Crear superusuario automáticamente al iniciar
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username = 'ADMIN'
    email = 'danielcccv2003@gmail.com'
    password = '12345'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f'Superuser "{username}" created successfully.')
    else:
        print(f'Superuser "{username}" already exists.')
except Exception as e:
    print(f'Error creating superuser: {e}')
