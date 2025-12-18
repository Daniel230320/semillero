from django import forms
from apps.compras.models import Compras, Detalle_compras
from apps.lotes.models import Detalle_compra_lotes

# Clase Formulario Compra
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compras
        fields = '__all__'

# Clase Formulario Detalle Compra
class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = Detalle_compras
        fields = '__all__'

# Clase Formulario Detalle Compra Lote
class DetalleCompraLoteForm(forms.ModelForm):
    class Meta:
        model = Detalle_compra_lotes
        fields = '__all__'