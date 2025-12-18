from django.db import models

# Clase Tipo de Documento
class Tipodocumentos(models.Model):
    idtipodocumento = models.AutoField(primary_key=True)
    descripcion_tipodocumento = models.CharField(max_length=25, verbose_name="Descripción")

    def __str__(self):
        return self.descripcion_tipodocumento
    
    class Meta:
        db_table="tipodocumentos"
        verbose_name="Tipo Documento"
        verbose_name_plural="Tipo Documentos"
    
# Clase Cliente
class Clientes(models.Model):
    idcliente = models.AutoField(primary_key=True)
    idtipodocumento = models.ForeignKey(Tipodocumentos, on_delete=models.PROTECT, verbose_name="Tipo de Identificación")
    numerodocumento = models.CharField(max_length=13, unique=True, verbose_name="Número de Identificación")
    nombre_cliente = models.CharField(max_length=60, verbose_name="Nombre")
    direccion_cliente = models.CharField(max_length=100, verbose_name="Dirección")
    correo_cliente = models.EmailField(max_length=80, unique=True, verbose_name="Correo")
    telefono_cliente = models.CharField(max_length=9, null=True, blank=True, verbose_name="Teléfono")
    celular_cliente = models.CharField(max_length=10, null=True, blank=True, verbose_name="Celular")
    estado_cliente = models.IntegerField(default=1, verbose_name="Estado")

    def __str__(self):
        return self.nombre_cliente
    
    class Meta:
        ordering = ['-estado_cliente']
        db_table="clientes"
        verbose_name="Cliente"
        verbose_name_plural="Clientes"
