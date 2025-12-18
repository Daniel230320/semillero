import django_filters
from apps.usuarios.models import CustomUser
from django.contrib.auth.models import Group
from django import forms

# Clase Filtro Usuario
class CustomUserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        lookup_expr='icontains', 
        label="Nombre de Usuario:", 
        widget=forms.TextInput(
            attrs={'placeholder': 'Buscar por nombre...'}
        ),
    )
    groups = django_filters.ModelChoiceFilter(
        queryset=Group.objects.all(), 
        label="Rol:", 
        empty_label="Todos los roles"
    )
    is_active = django_filters.ChoiceFilter(
        choices=[(True, "Activo"), (False, "Inactivo")], 
        label="Estado:", 
        empty_label="Todos los estados"
    ) 

    class Meta:
        model = CustomUser
        fields = ['username', 'groups', 'is_active']
