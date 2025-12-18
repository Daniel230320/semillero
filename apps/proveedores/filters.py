import django_filters
from apps.proveedores.models import Proveedores
from django import forms

# Clase Filtro Proveedor
class ProveedoresFilter(django_filters.FilterSet):
    nombre_proveedor = django_filters.CharFilter(
        lookup_expr='icontains', 
        label="Nombre del Proveedor:", 
        widget=forms.TextInput(
            attrs={'placeholder': 'Buscar por nombre...'}
        ),
    )
    estado_proveedor = django_filters.ChoiceFilter(
        choices=[(1, "Activo"), (0, "Inactivo")], 
        label="Estado:", 
        empty_label="Todos los estados"
    )

    class Meta:
        model = Proveedores
        fields = ['nombre_proveedor', 'estado_proveedor']