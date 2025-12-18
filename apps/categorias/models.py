from django.db import models

# Clase Categoria de Articulos
class Categoriaarticulos(models.Model):
    idcategoriaarticulo = models.AutoField(primary_key=True)
    descripcion_categoriaarticulo =models.CharField(max_length=100, verbose_name="Descripción")

    def __str__(self):
        return self.descripcion_categoriaarticulo
    
    class Meta:
        ordering = ['descripcion_categoriaarticulo']
        db_table="categoriaarticulos"
        verbose_name="Categoría Artículo"
        verbose_name_plural="Categoría Artículos"
    