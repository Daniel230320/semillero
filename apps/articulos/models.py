from django.db import models
from apps.categorias.models import Categoriaarticulos
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

# Clase Graba Iva
class Givas(models.Model):
    idgiva = models.AutoField(primary_key=True)
    descripcion_giva = models.CharField(max_length=30, verbose_name="Descripción")
    valoriva = models.IntegerField(verbose_name="Tasa de IVA (%)")

    def __str__(self):
        return self.descripcion_giva

    class Meta:
        db_table="givas"
        verbose_name="Graba Iva"
        verbose_name_plural="Graba Ivas"

# Clase Tipo Articulos
class TipoArticulos(models.Model):
    idtipoarticulo = models.AutoField(primary_key=True)
    descripcion_tipo = models.CharField(max_length=50, verbose_name="Descripción")

    def __str__(self):
        return self.descripcion_tipo

    class Meta:
        db_table="tipos_articulos"
        verbose_name="Tipo Artículo"
        verbose_name_plural="Tipos Artículos"

# Clase Niveles de Grasa
class NivelesGrasa(models.Model):
    idnivelgrasa = models.AutoField(primary_key=True)
    descripcion_ngrasa = models.CharField(max_length=50, verbose_name="Descripción")
    valor_nivel = models.IntegerField(verbose_name="Valor")

    def __str__(self):
        return self.descripcion_ngrasa

    class Meta:
        db_table="niveles_grasa"
        verbose_name="Nivel de Grasa"
        verbose_name_plural="Niveles de Grasa"

# Clase Niveles de Azucar
class NivelesAzucar(models.Model):
    idnivelazucar = models.AutoField(primary_key=True)
    descripcion_nazucar = models.CharField(max_length=50, verbose_name="Descripción")
    valor_nivel = models.IntegerField(verbose_name="Valor")

    def __str__(self):
        return self.descripcion_nazucar

    class Meta:
        db_table="niveles_azucar"
        verbose_name="Nivel de Azúcar"
        verbose_name_plural="Niveles de Azúcar"

# Clase Niveles de Sal
class NivelesSal(models.Model):
    idnivelsal = models.AutoField(primary_key=True)
    descripcion_nsal = models.CharField(max_length=50, verbose_name="Descripción")
    valor_nivel = models.IntegerField(verbose_name="Valor")

    def __str__(self):
        return self.descripcion_nsal

    class Meta:
        db_table="niveles_sal"
        verbose_name="Nivel de Sal"
        verbose_name_plural="Niveles de Sal"

# Clase Articulos
class Articulos(models.Model):
    idarticulo = models.AutoField(primary_key=True)
    codigoarticulo = models.CharField(max_length=15, unique=True, verbose_name="Código de Producto", help_text="Código interno del producto")
    idcategoriaarticulo = models.ForeignKey(Categoriaarticulos, on_delete=models.PROTECT, verbose_name="Categoría")
    idgiva = models.ForeignKey(Givas, on_delete=models.PROTECT, verbose_name="Graba Iva")
    idtipoarticulo = models.ForeignKey(TipoArticulos, on_delete=models.PROTECT, verbose_name="Tipo Producto")
    idnivelgrasa = models.ForeignKey(NivelesGrasa, on_delete=models.PROTECT, verbose_name="Nivel de Grasa", null=True, blank=True)
    idnivelazucar = models.ForeignKey(NivelesAzucar, on_delete=models.PROTECT, verbose_name="Nivel de Azúcar", null=True, blank=True)
    idnivelsal = models.ForeignKey(NivelesSal, on_delete=models.PROTECT, verbose_name="Nivel de Sal", null=True, blank=True)
    codigo_barras = models.CharField(max_length=13, unique=True, blank=True, null=True, help_text="Código de barras (EAN-13 generado o escaneado)")#nuevo
    imagen_barras = models.ImageField(upload_to='barcodes/', blank=True, null=True, verbose_name="Imagen de Código de barras")#nuevo
    imagen = models.ImageField(upload_to="imagenes/", null=True, blank=True, verbose_name="Imagen")
    descripcion_articulo = models.CharField(max_length=100, verbose_name="Descripción")
    tiene_semaforo = models.BooleanField(default=False, verbose_name="¿Tiene semáforo?")
    tiene_fecha_caduca = models.BooleanField(default=False, verbose_name="¿Tiene fecha de caducidad?")
    manejo_por_lotes = models.BooleanField(default=False, verbose_name="¿Se maneja por lotes?")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    stock_minimo = models.IntegerField(default=0, verbose_name="Stock Mínimo")
    stock_maximo = models.IntegerField(default=1, verbose_name="Stock Máximo")
    costo = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Costo ($)")
    utilidad = models.IntegerField(verbose_name="Utilidad (%)")
    precioventa = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Precio Venta ($)")
    estado_articulo = models.IntegerField(default=1, verbose_name="Estado")

    def __str__(self):
        return self.descripcion_articulo
    
    # Obtener el valor del IVA
    def get_valor_iva(self):
        return self.idgiva.valoriva

    # Eliminar las imagenes del directorio
    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name)
        return super().delete(using, keep_parents)
    
    # Generar el código de barras EAN-13
    def generar_imagen_barras(self):
        # Eliminar imagen anterior si existe
        if self.imagen_barras:
            self.imagen_barras.storage.delete(self.imagen_barras.name)
        
        # Generar nueva imagen
        ean = barcode.get('ean13', self.codigo_barras, writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        filename = f'barcode_{self.codigo_barras}.png'
        self.imagen_barras.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        # Verificar si el código de barras fue modificado
        if self.pk:  # Solo si el objeto ya existe
            original = self.__class__.objects.get(pk=self.pk)
            if original.codigo_barras != self.codigo_barras:
                self.generar_imagen_barras()
        
        # Generar imagen si no existe
        elif self.codigo_barras and not self.imagen_barras:
            self.generar_imagen_barras()
            
        super().save(*args, **kwargs)
    
    # Opciones adicionales
    class Meta:
        ordering = ['-estado_articulo', 'descripcion_articulo']
        db_table="articulos"
        verbose_name="Artículo"
        verbose_name_plural="Artículos"
    