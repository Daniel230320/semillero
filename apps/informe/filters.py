import django_filters
from apps.clientes.models import *
from apps.proveedores.models import *
from apps.articulos.models import *
from apps.ventas.models import *
from apps.compras.models import *
from apps.lotes.models import *
from django.forms import DateInput
from django.contrib.auth import get_user_model
User = get_user_model()

# Clase Filtro Reporte Ventas
class ReporteVentasFilter(django_filters.FilterSet):
    idcliente = django_filters.ModelChoiceFilter(
        queryset=Clientes.objects.all(), 
        label="Cliente:", 
        empty_label="Todos los clientes"
    )
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), 
        label="Usuario:", 
        empty_label="Todos los usuarios"
    )
    fecha_venta_desde = django_filters.DateFilter(
        field_name="fecha_venta", 
        lookup_expr='gte', 
        label="Fecha Desde:", 
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    fecha_venta_hasta = django_filters.DateFilter(
        field_name="fecha_venta", 
        lookup_expr='lte', 
        label="Fecha Hasta:", 
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    
    class Meta:
        model = Ventas
        fields = ['idcliente', 'user']


# Clase Filtro Reporte Compras
class ReporteComprasFilter(django_filters.FilterSet):
    idproveedor = django_filters.ModelChoiceFilter(
        queryset=Proveedores.objects.all(), 
        label="Proveedor:", 
        empty_label="Todos los proveedores"
    )
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), 
        label="Usuario:", 
        empty_label="Todos los usuarios"
    )
    fecha_compra_desde = django_filters.DateFilter(
        field_name="fecha_compra", 
        lookup_expr='gte', 
        label="Fecha Desde:", 
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    fecha_compra_hasta = django_filters.DateFilter(
        field_name="fecha_compra", 
        lookup_expr='lte', 
        label="Fecha Hasta:", 
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    
    class Meta:
        model = Compras
        fields = ['idproveedor', 'user']


# Clase Filtro Reporte Inventario
class ReporteInventarioFilter(django_filters.FilterSet):
    descripcion_articulo = django_filters.ModelChoiceFilter(
        queryset=Articulos.objects.all(), 
        label="Producto:", 
        empty_label="Todos los productos"
    )
    idcategoriaarticulo = django_filters.ModelChoiceFilter(
        queryset=Categoriaarticulos.objects.all(), 
        label="Categoría:", 
        empty_label="Todas las categorias"
    )
    estado_articulo = django_filters.ChoiceFilter(
        choices=[(1, "Activo"), (0, "Inactivo")], 
        label="Estado del Producto:", 
        empty_label="Todos los estados"
    )
    
    class Meta:
        model = Articulos
        fields = ['descripcion_articulo', 'idcategoriaarticulo', 'estado_articulo']


# Clase Filtro Reporte Productos Caducos
class ReporteProductosCaducosFilter(django_filters.FilterSet):
    descripcion_articulo = django_filters.ModelChoiceFilter(
        queryset=Articulos.objects.all().filter(tiene_fecha_caduca=True),
        label="Producto:",
        empty_label="Todos los productos",
        field_name='codigoarticulo',
        to_field_name='idarticulo'
    )
    idcategoriaarticulo = django_filters.ModelChoiceFilter(
        queryset=Categoriaarticulos.objects.all(),
        label="Categoría:",
        empty_label="Todas las categorías",
        field_name='codigoarticulo__idcategoriaarticulo'
    )
    idestado_lote = django_filters.ModelChoiceFilter(
        queryset=Estado_lotes.objects.all().exclude(code_estado_lote='no_vence'),
        label="Estado del Lote:",
        empty_label="Todos los estados"
    )
    fecha_caducidad_desde = django_filters.DateFilter(
        field_name="fecha_caducidad",
        lookup_expr='gte',
        label="Fecha Caducidad Desde:",
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    fecha_caducidad_hasta = django_filters.DateFilter(
        field_name="fecha_caducidad",
        lookup_expr='lte',
        label="Fecha Caducidad Hasta:",
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    idlote = django_filters.ModelChoiceFilter(
        queryset=Lotes.objects.all(),
        label="Lote:",
        empty_label="Todos los lotes"
    )

    class Meta:
        model = Lotes
        fields = ['descripcion_articulo', 'idcategoriaarticulo', 'idestado_lote']
