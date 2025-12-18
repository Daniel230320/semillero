import django_filters
from apps.articulos.models import Articulos, Categoriaarticulos
from apps.articulos.models import Givas
from django import forms
from django.forms import NumberInput

# Clase Filtro Articulo
class ArticulosFilter(django_filters.FilterSet):
    descripcion_articulo = django_filters.CharFilter(
        lookup_expr='icontains', 
        label="Nombre del Producto:", 
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por nombre...'}),
    )
    idcategoriaarticulo = django_filters.ModelChoiceFilter(
        queryset=Categoriaarticulos.objects.all(), 
        label="Categoría:", 
        empty_label="Todos las categorias"
    )
    idgiva = django_filters.ModelChoiceFilter(
        queryset=Givas.objects.all(), 
        label="Graba IVA:", 
        empty_label="Todos los tipos"
    )
    stock_min = django_filters.NumberFilter(
        field_name="stock", 
        lookup_expr="gte", 
        label="Rango Mínimo:", 
        widget=NumberInput(attrs={'placeholder': 'Stock', 'min': 0}),
    )
    stock_max = django_filters.NumberFilter(
        field_name="stock", 
        lookup_expr="lte", 
        label="Rango Máximo:", 
        widget=NumberInput(attrs={'placeholder': 'Stock', 'min': 0}),
    )
    estado_articulo = django_filters.ChoiceFilter(
        choices=[(1, "Activo"), (0, "Inactivo")], 
        label="Estado:", 
        empty_label="Todos los estados"
    )

    class Meta:
        model = Articulos
        fields = ['descripcion_articulo', 'idcategoriaarticulo', 'idgiva', 'estado_articulo']