from django.forms import ModelForm, ValidationError
from apps.empresa.models import Ciudades, Provincias, Empresas
from django import forms

# Clase Formulario Empresa
class EmpresaForm(ModelForm):
    idprovincia = forms.ModelChoiceField(
        queryset = Provincias.objects.all().order_by('nombre_provincia'), 
        label='Provincia', 
        required=True, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ), 
        empty_label="Seleccione una provincia"
    )

    idciudad = forms.ModelChoiceField(
        queryset=Ciudades.objects.none(), 
        label='Ciudad', 
        required=True, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ), 
        empty_label="Seleccione una ciudad"
    )
    
    # Validación de los campos
    def clean_RUC(self):
        RUC=self.cleaned_data["RUC"]
        if not RUC.isdigit() or len(RUC) != 13:
            raise ValidationError("El RUC debe contener solo 13 dígitos numéricos")
        return RUC

    def clean_cedularepresentantelegal(self):
        ceduRepr=self.cleaned_data["cedularepresentantelegal"]
        if not ceduRepr.isdigit() or len(ceduRepr) != 10:
            raise ValidationError("La cedula debe contener solo 10 dígitos numéricos")
        return ceduRepr
    
    def clean_stock_minimo_general(self):
        activar_notif_stock = self.cleaned_data["activar_notif_stock"]
        if activar_notif_stock:
            stock_minimo = self.cleaned_data["stock_minimo_general"]
            if stock_minimo is None:
                raise ValidationError("Este campo es requerido")
            return stock_minimo
        
    def clean_stock_maximo_general(self):
        activar_notif_stock = self.cleaned_data["activar_notif_stock"]
        if activar_notif_stock:
            stock_maximo = self.cleaned_data["stock_maximo_general"]
            stock_minimo = self.cleaned_data.get("stock_minimo_general")
            
            if stock_maximo is None:
                raise ValidationError("Este campo es requerido")
            if stock_minimo is None:
                raise ValidationError("Primero debe establecer un stock mínimo válido")
            if stock_maximo <= stock_minimo:
                raise ValidationError("El stock máximo debe ser mayor que el stock mínimo")
            return stock_maximo
        
    def clean_dias_por_vencer_general(self):
        activar_notif_por_vencer = self.cleaned_data["activar_notif_por_vencer"]
        if activar_notif_por_vencer:
            dias_por_vencer = self.cleaned_data["dias_por_vencer_general"]
            if dias_por_vencer is None:
                raise ValidationError("Este campo es requerido")
            if dias_por_vencer <= 1:
                raise ValidationError("El número de días debe ser mayor que 1")
            return dias_por_vencer
    
    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)

        # Personalización de los widgets
        self.fields['RUC'].widget.attrs.update({'placeholder': 'Ingresa el RUC'})
        self.fields['razonsocial'].widget.attrs.update({'placeholder': 'Ingresa la razón social'})
        self.fields['nombrecomercial'].widget.attrs.update({'placeholder': 'Ingresa el nombre comercial'})
        self.fields['direccion1'].widget.attrs.update({'placeholder': 'Ingresa la dirección'})
        self.fields['direccion2'].widget.attrs.update({'placeholder': 'Ingresa la dirección'})
        self.fields['correo_empresa'].widget.attrs.update({'placeholder': 'Ingresa el correo electrónico'})
        self.fields['telefono_empresa'].widget.attrs.update({'placeholder': 'Ingresa el teléfono'})
        self.fields['celular_empresa'].widget.attrs.update({'placeholder': 'Ingresa el celular'})
        self.fields['cedularepresentantelegal'].widget.attrs.update({'placeholder': 'Ingresa la cédula del representante legal'})
        self.fields['nombrerepresentantelegal'].widget.attrs.update({'placeholder': 'Ingresa el nombre del representante legal'})
        self.fields['stock_minimo_general'].widget.attrs.update({'placeholder': 'Ingresa el stock mínimo'})
        self.fields['stock_maximo_general'].widget.attrs.update({'placeholder': 'Ingresa el stock máximo'})
        self.fields['dias_por_vencer_general'].widget.attrs.update({'placeholder': 'Ingresa los días por vencer'})

        # Configuración de los selectores de provincia y ciudad
        self.fields['idciudad'].queryset = Ciudades.objects.none()
        if 'idprovincia' in self.data:
            try:
                provincia_id = int(self.data.get('idprovincia'))
                self.fields['idciudad'].queryset = (
                    Ciudades.objects
                    .filter(idprovincia=provincia_id)
                    .order_by('nombre_ciudad')
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.idciudad:
            self.fields['idprovincia'].initial = self.instance.idciudad.idprovincia.pk
            self.fields['idciudad'].queryset = (
                Ciudades.objects
                .filter(idprovincia=self.instance.idciudad.idprovincia)
                .order_by('nombre_ciudad')
            )
            self.fields['idprovincia'].widget.attrs['disabled'] = False
    
    class Meta:
        model = Empresas
        fields = '__all__'
        exclude = ['idempresa', 'estado_empresa', 'rutaarchivogenerados']
    