from django import forms
from apps.ventas.models import Ventas, Detalle_ventas, Formapagos, Pagos

# Clase Formulario Venta
class VentaForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = '__all__'

# Clase Formulario Detalle Venta
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = Detalle_ventas
        fields = '__all__'

# Clase Formulario Forma Pago
class FormaPagoForm(forms.ModelForm):
    class Meta:
        model = Formapagos
        fields = '__all__'

# Clase Formulario Pago
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pagos
        fields = '__all__'
