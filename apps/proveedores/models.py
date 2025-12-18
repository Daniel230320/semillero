from django.db import models

# Clase Proveedor
class Proveedores(models.Model):
    idproveedor = models.AutoField(primary_key=True)
    ruc_proveedor = models.CharField(max_length=13, unique=True, verbose_name="RUC")
    nombrecontacto_proveedor = models.CharField(max_length=60, verbose_name="Contacto")
    nombre_proveedor = models.CharField(max_length=60, verbose_name="Nombre")
    direccion_proveedor = models.CharField(max_length=100, verbose_name="Dirección")
    correo_proveedor = models.EmailField(max_length=80, unique=True, verbose_name="Correo")
    telefono_proveedor = models.CharField(max_length=9, null=True, blank=True, verbose_name="Teléfono")
    celular_proveedor = models.CharField(max_length=10, null=True, blank=True, verbose_name="Celular")
    estado_proveedor = models.IntegerField(default=1, verbose_name="Estado")

    def __str__(self):
        return self.nombre_proveedor
    
    class Meta:
        ordering = ['-estado_proveedor', 'nombre_proveedor']
        db_table="proveedores"
        verbose_name="Proveedor"
        verbose_name_plural="Proveedores"
