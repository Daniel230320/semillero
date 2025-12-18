from django import forms
from apps.clientes.models import Clientes
from django.forms import ModelForm, ValidationError

# Clase Formulario Cliente
class ClienteForm(ModelForm):
    ESTADO_CHOICES = ((0, 'Inactivo'), (1, 'Activo'),)
    estado_cliente = forms.ChoiceField(choices=ESTADO_CHOICES, label='Estado', initial=1)

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        
        # Personalización de los widgets
        self.original_numerodocumento = self.instance.numerodocumento if self.instance else None
        self.fields['idtipodocumento'].initial = 2
        self.fields['idtipodocumento'].empty_label = "Seleccione un tipo de identificación"
        self.fields['nombre_cliente'].widget.attrs.update({'placeholder': 'Ingresa el nombre'})
        self.fields['numerodocumento'].widget.attrs.update({'placeholder': 'Ingresa el número de identificación'})
        self.fields['direccion_cliente'].widget.attrs.update({'placeholder': 'Ingresa la dirección'})
        self.fields['correo_cliente'].widget.attrs.update({'placeholder': 'Ingresa el correo electrónico'})
        self.fields['telefono_cliente'].widget.attrs.update({'placeholder': 'Ingresa el teléfono'})
        self.fields['celular_cliente'].widget.attrs.update({'placeholder': 'Ingresa el celular'})

    # Validación de los campos
    def clean_numerodocumento(self):
        numerodocumento=self.cleaned_data["numerodocumento"]
        idtipodocumento=self.cleaned_data["idtipodocumento"]
        if idtipodocumento.idtipodocumento == 1:
            if not numerodocumento.isdigit() or len(numerodocumento) != 13:
                raise ValidationError("El RUC debe contener solo 13 dígitos numéricos")
            if not numerodocumento.endswith("001"):
                raise ValidationError("El RUC debe terminar en '001'")
        elif idtipodocumento.idtipodocumento == 2:
            if not numerodocumento.isdigit() or len(numerodocumento) != 10:
                raise ValidationError("La cédula debe contener solo 10 dígitos numéricos")
        else :
            if not numerodocumento.isdigit() or len(numerodocumento) < 10:
                raise ValidationError("El pasaporte debe contener entre 10 y 13 dígitos numéricos")
        return numerodocumento

    class Meta:
        model = Clientes 
        fields = '__all__'
        exclude = ['idcliente']