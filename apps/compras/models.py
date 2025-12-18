from django.db import models
from apps.usuarios.models import CustomUser
from apps.proveedores.models import Proveedores
from apps.articulos.models import Articulos

# Clase Compra
class Compras(models.Model):
    idcompra = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, verbose_name="Usuario")
    idproveedor = models.ForeignKey(Proveedores, on_delete=models.PROTECT, verbose_name="Proveedor")
    concepto = models.CharField(max_length=100, null=True, blank=True, verbose_name="Concepto") 
    fecha_compra = models.DateField(verbose_name="Fecha")
    subtotal_tarifa0 = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Tarifa 0")
    subtotal_tarifa12 = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Tarifa 15")
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Subtotal")
    valoriva = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor IVA")
    total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total")
    estado_compra = models.IntegerField(default=1, verbose_name="Estado")

    def __str__(self):
        return self.concepto
    
    class Meta:
        ordering = ['-idcompra', '-fecha_compra']
        db_table="compras"
        verbose_name="Compra"
        verbose_name_plural="Compras"

# Clase Detalle de la Compra
class Detalle_compras(models.Model):
    iddetalle_compra = models.AutoField(primary_key=True)
    idcompra = models.ForeignKey(Compras, on_delete=models.RESTRICT, verbose_name="Compra")
    codigoarticulo = models.ForeignKey(Articulos, on_delete=models.RESTRICT, verbose_name="Artículo")
    preciounitario = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Precio Unitario")
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor")
    #valor_total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Total")
    cantidad = models.IntegerField(verbose_name="Cantidad")

    def __str__(self):
        return f'{self.idcompra} - {self.codigoarticulo}'
    
    class Meta:
        db_table="detalle_compras"
        verbose_name="Detalle Compra"
        verbose_name_plural="Detalle Compras"

