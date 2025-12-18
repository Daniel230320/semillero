import django_filters
from apps.clientes.models import Clientes
from apps.ventas.models import Ventas
from django.forms import NumberInput, DateInput
from django.contrib.auth import get_user_model

User = get_user_model()

# Clase Filtro Venta
class VentasFilter(django_filters.FilterSet):
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
    estado_venta = django_filters.ChoiceFilter(
        choices=[(1, "Completado"), (0, "No disponible")], 
        label="Estado:", 
        empty_label="Todos los estados"
    )
    total_min = django_filters.NumberFilter(
        field_name="total", 
        lookup_expr="gte", 
        label="Rango Mínimo:", 
        widget=NumberInput(
            attrs={'placeholder': 'Total Venta', 'min': 0, 'step': '0.01'}
        )
    )
    total_max = django_filters.NumberFilter(
        field_name="total", 
        lookup_expr="lte", 
        label="Rango Máximo:", 
        widget=NumberInput(
            attrs={'placeholder': 'Total Venta', 'min': 0, 'step': '0.01'}
        )
    )
    fecha_venta_desde = django_filters.DateFilter(
        field_name="fecha_venta", 
        lookup_expr='gte', 
        label="Desde:", 
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
    fecha_venta_hasta = django_filters.DateFilter(
        field_name="fecha_venta", 
        lookup_expr='lte', 
        label="Hasta:", 
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Ventas
        fields = ['idcliente', 'user', 'estado_venta']
