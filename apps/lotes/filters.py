import django_filters
from apps.lotes.models import Lotes, Estado_lotes
from apps.articulos.models import Articulos

# Clase Filtro Lote
class LoteFilter(django_filters.FilterSet):
    producto = django_filters.ModelChoiceFilter(
        queryset=Articulos.objects.filter(manejo_por_lotes=True), 
        field_name='codigoarticulo', 
        label='Producto:', 
        empty_label="Todos los productos"
    )
    estado = django_filters.ModelChoiceFilter(
        queryset=Estado_lotes.objects.all(), 
        field_name='idestado_lote', 
        label='Estado:', 
        empty_label="Todos los estados"
    )

    class Meta:
        model = Lotes
        fields = ['producto', 'estado']