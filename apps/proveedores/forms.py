from django.forms import ModelForm, ValidationError
from apps.proveedores.models import Proveedores
from django import forms

# Clase Formulario Proveedor
class ProveedorForm(ModelForm):
    ESTADO_CHOICES = ((0, 'Inactivo'), (1, 'Activo'),)
    estado_proveedor = forms.ChoiceField(choices=ESTADO_CHOICES, label='Estado', initial=1)

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        
        # Personalización de los widgets
        self.fields['nombrecontacto_proveedor'].widget.attrs.update({'placeholder': 'Ingresa el nombre de contacto'})
        self.fields['nombre_proveedor'].widget.attrs.update({'placeholder': 'Ingresa el nombre'})
        self.fields['ruc_proveedor'].widget.attrs.update({'placeholder': 'Ingresa el RUC'})
        self.fields['direccion_proveedor'].widget.attrs.update({'placeholder': 'Ingresa la dirección'})
        self.fields['correo_proveedor'].widget.attrs.update({'placeholder': 'Ingresa el correo electrónico'})
        self.fields['telefono_proveedor'].widget.attrs.update({'placeholder': 'Ingresa el teléfono'})
        self.fields['celular_proveedor'].widget.attrs.update({'placeholder': 'Ingresa el celular'})

    # Validación de los campos
    def clean_ruc_proveedor(self):
        ruc_proveedor = self.cleaned_data.get("ruc_proveedor")
        if not ruc_proveedor.isdigit() or len(ruc_proveedor) != 13:
            raise ValidationError("El RUC debe contener solo 13 dígitos numéricos")
        if not ruc_proveedor.endswith("001"):
            raise ValidationError("El RUC debe terminar en '001'")
        return ruc_proveedor

    class Meta:
        model = Proveedores
        fields = '__all__'
        exclude = ['idproveedor']