from django.forms import ModelForm
from django.contrib.auth.models import Group, Permission
from django import forms

# Clase Formulario Grupo (roles)
class GroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Ingresa el nombre'})

    class Meta:
        model = Group
        fields = ['name']
        #widgets = {'permissions': forms.CheckboxSelectMultiple}


# Clase Formulario Permiso (permisos de usuarios en roles)
class PermisoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermisoForm, self).__init__(*args, **kwargs)
        
        # Filtrar los permisos
        permisos_filtrados = Permission.objects.filter(id__gte=97).order_by('id') # Filtrar los permisos con ID mayor
        choices = [(permiso.id, permiso.name) for permiso in permisos_filtrados]  # Crea una lista de tuplas (valor, etiqueta)
        self.fields['permissions'].queryset = permisos_filtrados
        self.fields['permissions'].choices = choices

    class Meta:
        model = Group
        fields = ['permissions']
        widgets = {'permissions': forms.CheckboxSelectMultiple(
                attrs={'class': 'custom-control-input'}
            )
        }
    