from django.db import models
from django.contrib.auth.models import AbstractUser

# Clase Usuario (Personalizada)
class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=15, verbose_name="Nombre de usuario", help_text='Únicamente letras, dígitos y @/./+/-/_')
    first_name = models.CharField(max_length=30, verbose_name="Nombres")
    last_name = models.CharField(max_length=40, verbose_name="Apellidos")
    email = models.EmailField(unique=True, max_length=100, verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=9, null=True, blank=True, verbose_name="Teléfono")
    celular = models.CharField(max_length=10, null=True, blank=True, verbose_name="Celular")
    direccion = models.CharField(max_length=100, null=True, blank=True, verbose_name="Dirección")

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['-is_active', 'first_name', 'last_name']
        db_table = "auth_user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
