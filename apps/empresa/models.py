from django.db import models

# Clase Provincia
class Provincias(models.Model):
    idprovincia = models.AutoField(primary_key=True)
    nombre_provincia = models.CharField(max_length=50, verbose_name="Nombre")

    def __str__(self):
        return self.nombre_provincia
    
    class Meta:
        db_table="provincias"
        verbose_name="Provincia"
        verbose_name_plural="Provincias"            

# Clase Ciudad
class Ciudades(models.Model):
    idciudad = models.AutoField(primary_key=True)
    idprovincia = models.ForeignKey(Provincias, on_delete=models.PROTECT, verbose_name="Provincia")
    nombre_ciudad = models.CharField(max_length=50, verbose_name="Nombre")

    def __str__(self):
        return self.nombre_ciudad
    
    class Meta:
        db_table="ciudades"
        verbose_name="Ciudad"
        verbose_name_plural="Ciudades"
    
# Clase Empresa
class Empresas(models.Model):
    # NUEVO
    NOTIFICAR_A_OPCIONES = [
        ('todos', 'Todos los usuarios'),
        ('superuser', 'Solo el Administrador Principal'),
    ]

    idempresa = models.AutoField(primary_key=True)
    idciudad = models.ForeignKey(Ciudades, on_delete=models.PROTECT, verbose_name="Ciudad")
    RUC = models.CharField(max_length=13, verbose_name="RUC")
    razonsocial = models.CharField(max_length=80, verbose_name="Razón Social")
    nombrecomercial = models.CharField(max_length=80, verbose_name="Nombre Comercial")
    logo = models.ImageField(upload_to="imagenes/", null=True, blank=True, verbose_name="Logo de la Empresa")
    direccion1 = models.CharField(max_length=100, verbose_name="Dirección Matriz")
    direccion2 = models.CharField(max_length=100, verbose_name="Dirección Sucursal")
    correo_empresa = models.EmailField(max_length=80, verbose_name="Correo")
    telefono_empresa = models.CharField(max_length=9, null=True, blank=True, verbose_name="Teléfono")
    celular_empresa = models.CharField(max_length=10, null=True, blank=True, verbose_name="Celular")
    cedularepresentantelegal = models.CharField(max_length=10, verbose_name="Cedula Representante Legal")
    nombrerepresentantelegal = models.CharField(max_length=50, verbose_name="Nombre Representante Legal")
    rutaarchivogenerados = models.CharField(max_length=100, verbose_name="Ruta de Archivos")
    estado_empresa = models.IntegerField(default=1, verbose_name="Estado")

    # NUEVOS CAMPOS DE CONFIGURACIÓN
    notificar_a = models.CharField(
        max_length=10,
        choices=NOTIFICAR_A_OPCIONES,
        default='todos',
        verbose_name="Habilitar Notificaciones para"
    )
    activar_notif_stock = models.BooleanField(default=False, verbose_name="Notificación por stock de productos")
    stock_minimo_general = models.PositiveIntegerField(null=True, blank=True, verbose_name="Stock mínimo general")
    stock_maximo_general = models.PositiveIntegerField(null=True, blank=True, verbose_name="Stock máximo general")
    activar_notif_por_vencer = models.BooleanField(default=False, verbose_name="Notificación por vencer de productos")
    dias_por_vencer_general = models.PositiveIntegerField(null=True, blank=True, verbose_name="Días antes de vencer (general)")

    def __str__(self):
        return self.nombrecomercial
    
    # Eliminar las imagenes del directorio
    def delete(self, using=None, keep_parents=False):
        self.logo.storage.delete(self.logo.name)
        return super().delete()
    
    class Meta:
        db_table="datos_empresa"
        verbose_name="Empresa"
        verbose_name_plural="Empresas"
