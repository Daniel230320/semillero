import django_filters
from apps.notificaciones.models import NotificationCustomUser, Level
from apps.articulos.models import Articulos

# Clase Filtro Notificación
class NotificationCustomUserFilter(django_filters.FilterSet):
    idlevel = django_filters.ModelChoiceFilter(
        field_name='idnotification__idlevel', 
        queryset=Level.objects.all(), 
        label="Nivel:", 
        empty_label="Todos los niveles"
    )
    read = django_filters.ChoiceFilter(
        field_name='read', 
        label="Leída:", 
        choices=[(True, 'Sí'), (False, 'No')], 
        empty_label="Todos los estados"
    )
    target_object = django_filters.ModelChoiceFilter(
        queryset=Articulos.objects.all(), 
        label="Producto:", 
        empty_label="Todos los productos", 
        method='filter_by_articulo'
    )

    # Filtro por artículo
    def filter_by_articulo(self, queryset, name, value):
        if value:
            return queryset.filter(target_id=value.idarticulo)
        return queryset

    class Meta:
        model = NotificationCustomUser
        fields = ['idlevel', 'read', 'target_object']