from django.db import models
from apps.usuarios.models import CustomUser
from apps.clientes.models import Clientes
from apps.articulos.models import Articulos

# Clase Venta
class Ventas(models.Model):
    idventa = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, verbose_name="Usuario")
    idcliente = models.ForeignKey(Clientes, on_delete=models.PROTECT, verbose_name="Cliente")
    concepto = models.CharField(max_length=100, null=True, blank=True, verbose_name="Concepto") 
    fecha_venta = models.DateField(verbose_name="Fecha")
    subtotal_tarifa0 = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Tarifa 0")
    subtotal_tarifa12 = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Tarifa 15")
    descuento = models.DecimalField(default=0.00, max_digits=15, decimal_places=2, verbose_name="Descuento")
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Subtotal")
    valoriva = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor IVA")
    total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total")
    estado_venta = models.IntegerField(default=1, verbose_name="Estado")

    def __str__(self):
        return self.concepto
    
    class Meta:
        ordering = ['-idventa', '-fecha_venta']
        db_table="ventas"
        verbose_name="Venta"
        verbose_name_plural="Ventas"
    

# Clase Detalle Venta
class Detalle_ventas(models.Model):
    iddetalle_venta = models.AutoField(primary_key=True)
    idventa = models.ForeignKey(Ventas, on_delete=models.RESTRICT, verbose_name="Venta")
    codigoarticulo = models.ForeignKey(Articulos, on_delete=models.RESTRICT, verbose_name="Artículo")
    preciounitario = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Precio Unitario")
    valordescuento = models.DecimalField(default=0.00, max_digits=15, decimal_places=2, verbose_name="Valor Dscto")
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor")
    #valor_total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Total")
    cantidad = models.IntegerField(verbose_name="Cantidad")

    def __str__(self):
        return f'{self.idventa} - {self.codigoarticulo}'
    
    class Meta:
        db_table="detalle_ventas"
        verbose_name="Detalle Venta"
        verbose_name_plural="Detalle Ventas"


# Clase Forma de Pago
class Formapagos(models.Model):
    idformapago = models.AutoField(primary_key=True)
    descripcion_formapago = models.CharField(max_length=60, verbose_name="Descripción") 
    
    def __str__(self):
        return f'{self.descripcion_formapago}'
    
    class Meta:
        db_table="formapagos"
        verbose_name="Forma Pago"
        verbose_name_plural="Forma Pagos"


# Clase Pago
class Pagos(models.Model):
    idpago = models.AutoField(primary_key=True)
    idventa = models.ForeignKey(Ventas, on_delete=models.RESTRICT, verbose_name="Venta")
    idformapago = models.ForeignKey(Formapagos, on_delete=models.RESTRICT, verbose_name="Forma Pago")
    monto = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Monto")

    def __str__(self):
        return f'{self.idpago}'
    
    class Meta:
        db_table="pagos"
        verbose_name="Pago"
        verbose_name_plural="Pagos"
