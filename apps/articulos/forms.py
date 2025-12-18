from django.forms import ModelForm, ValidationError
from apps.articulos.models import Articulos, Givas
from django import forms
from decimal import Decimal


# Clase Formulario de Graba Iva
class GivasForm(ModelForm):
    def clean_valoriva(self):
        valoriva = self.cleaned_data.get('valoriva')
        if valoriva < 0:
            raise ValidationError("El valor del IVA no puede ser menor que 0")
        if valoriva > 99:
            raise ValidationError("El valor del IVA no puede ser mayor que 99")
        return valoriva
    
    def __init__(self, *args, **kwargs):
        super(GivasForm, self).__init__(*args, **kwargs)
        # Personalización de los widgets
        self.fields['valoriva'].widget.attrs.update({'min': '0', 'max': '100', 'placeholder': 'Ingresa el valor del IVA'})
        self.fields['descripcion_giva'].widget.attrs.update({'placeholder': 'Ingresa la descripción del IVA'})

    class Meta:
        model = Givas
        fields = '__all__'

# Clase Formulario Articulo
class ArticulosForm(ModelForm):
    ESTADO_CHOICES = ((0, 'Inactivo'), (1, 'Activo'),)
    estado_articulo = forms.ChoiceField(
        choices=ESTADO_CHOICES, 
        label="Estado", 
        initial=1
    )

    def __init__(self, *args, **kwargs):
        super(ArticulosForm, self).__init__(*args, **kwargs)

        # Personalización de los widgets
        self.fields['idcategoriaarticulo'].empty_label = "Seleccione una categoría"
        self.fields['idnivelgrasa'].empty_label = "Seleccione un nivel"
        self.fields['idnivelazucar'].empty_label = "Seleccione un nivel"
        self.fields['idnivelsal'].empty_label = "Seleccione un nivel"
        self.fields['idgiva'].empty_label = "Seleccione un tipo"
        self.fields['descripcion_articulo'].widget.attrs.update({'placeholder': 'Ingresa el nombre del producto'})
        self.fields['codigoarticulo'].widget.attrs.update({'placeholder': 'Ingresa el código del producto'})
        self.fields['codigo_barras'].widget.attrs.update({'placeholder': 'Código de barras del producto'})
        self.fields['tiene_semaforo'].widget.attrs.update({'class': 'custom-control-input'})
        self.fields['tiene_fecha_caduca'].widget.attrs.update({'class': 'custom-control-input'})
        self.fields['manejo_por_lotes'].widget.attrs.update({'class': 'custom-control-input'})
        self.fields['utilidad'].widget.attrs.update({'min': '0', 'max': '100', 'placeholder': 'Ingresa la utilidad'})
        self.fields['costo'].widget.attrs.update({'placeholder': 'Ingresa el costo'})
        self.fields['precioventa'].widget.attrs.update({'readonly': 'readonly', 'style': 'cursor: not-allowed;'})
        self.fields['stock_minimo'].widget.attrs.update({'placeholder': 'Ingresa un stock mínimo'})
        self.fields['stock_maximo'].widget.attrs.update({'placeholder': 'Ingresa un stock máximo'})

    # Validación de los campos
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def clean_tiene_semaforo(self):
        idtipoarticulo = self.cleaned_data['idtipoarticulo']
        tiene_semaforo = self.cleaned_data['tiene_semaforo']
        if idtipoarticulo.idtipoarticulo == 1:
            if not tiene_semaforo:
                raise ValidationError("El campo 'Habilitar Semáforo Nutricional' es obligatorio.")
        if tiene_semaforo and (not self.cleaned_data['idnivelgrasa'] or not self.cleaned_data['idnivelazucar'] or not self.cleaned_data['idnivelsal']):
            raise ValidationError("Al habilitar el semáforo nutricional, debes seleccionar cada nivel nutricional.")
        return tiene_semaforo

    def clean_utilidad(self):
        utilidad = self.cleaned_data.get('utilidad')
        if int(utilidad) < 0:
            raise ValidationError("El porcentaje de utilidad no puede ser negativo")
        if int(utilidad) > 99:
            raise ValidationError("El porcentaje de utilidad no puede ser mayor que 99")
        return utilidad

    def clean_costo(self):
        costo = self.cleaned_data.get('costo')
        if Decimal(costo) < Decimal('0.00'):
            raise ValidationError("El costo no puede ser negativo")
        return costo
    
    def clean_precioventa(self):
        precioventa = self.cleaned_data.get('precioventa')
        if Decimal(precioventa) < Decimal('0.00'):
            raise ValidationError("El precio de venta no puede ser negativo")
        return precioventa
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        max_size = 4 * 1024 * 1024  # 3 MB en bytes
        if imagen and imagen.size > max_size:
            raise ValidationError("El tamaño máximo de la imagen debe ser de 4 MB.")
        return imagen
    
    def clean_manejo_por_lotes(self):
        manejo_por_lotes = self.cleaned_data.get('manejo_por_lotes')
        tiene_fecha_caduca = self.cleaned_data.get('tiene_fecha_caduca')
        if tiene_fecha_caduca and not manejo_por_lotes:
            raise ValidationError("Si seleccionas 'Tiene fecha de caducidad', debes seleccionar 'Manejo por lotes'.")
        return manejo_por_lotes
    
    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo < 0:
            raise ValidationError("El stock mínimo no puede ser negativo")
        return stock_minimo

    def clean_stock_maximo(self):
        stock_maximo = self.cleaned_data.get('stock_maximo')
        stock_minimo = self.cleaned_data.get('stock_minimo')
        errors = []
        if stock_maximo is not None and stock_minimo is not None:
            if stock_maximo <= stock_minimo:
                errors.append("El stock máximo debe ser mayor que el stock mínimo")
        if stock_maximo < 0:
            errors.append("El stock máximo no puede ser negativo")
        if errors:
            raise ValidationError(errors)
        return stock_maximo

    class Meta:
        model = Articulos
        fields = '__all__'
        exclude = ['idarticulo', 'stock']