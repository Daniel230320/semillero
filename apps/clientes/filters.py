import django_filters
from django import forms
from apps.clientes.models import Clientes, Tipodocumentos

# Clase Filtro Cliente
class ClientesFilter(django_filters.FilterSet):
    nombre_cliente = django_filters.CharFilter(
        lookup_expr='icontains', 
        label="Nombre del Cliente:", 
        widget=forms.TextInput(
            attrs={'placeholder': 'Buscar por nombre...'}
        ),
    )
    idtipodocumento = django_filters.ModelChoiceFilter(
        queryset=Tipodocumentos.objects.all(), 
        label="Tipo de Identificación:", 
        empty_label="Todos los tipos"
    )
    estado_cliente = django_filters.ChoiceFilter(
        choices=[(1, "Activo"), (0, "Inactivo")], 
        label="Estado:", 
        empty_label="Todos los estados"
    )

    class Meta:
        model = Clientes
        fields = ['nombre_cliente', 'idtipodocumento', 'estado_cliente']