import django_filters
from apps.proveedores.models import Proveedores
from apps.compras.models import Compras
from django.forms import NumberInput, DateInput
from django.contrib.auth import get_user_model

User = get_user_model()

# Clase Filtro Compra
class ComprasFilter(django_filters.FilterSet):
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
    estado_compra = django_filters.ChoiceFilter(
        choices=[(1, "Completado"), (0, "No disponible")], 
        label="Estado:", 
        empty_label="Todos los estados"
    )
    total_min = django_filters.NumberFilter(
        field_name="total", 
        lookup_expr="gte", 
        label="Rango Mínimo:", 
        widget=NumberInput(
            attrs={'placeholder': 'Total Compra', 'min': 0, 'step': '0.01'}
        )
    )
    total_max = django_filters.NumberFilter(
        field_name="total", 
        lookup_expr="lte", 
        label="Rango Máximo:", 
        widget=NumberInput(
            attrs={'placeholder': 'Total Compra', 'min': 0, 'step': '0.01'}
        )
    )
    fecha_compra_desde = django_filters.DateFilter(
        field_name="fecha_compra", 
        lookup_expr='gte', 
        label="Desde:", 
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    fecha_compra_hasta = django_filters.DateFilter(
        field_name="fecha_compra", 
        lookup_expr='lte', 
        label="Hasta:", 
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    
    class Meta:
        model = Compras
        fields = ['idproveedor', 'user', 'estado_compra']
