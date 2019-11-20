from django import forms

from .models import Compra
from ..producto.models import Producto


class CompraForm(forms.ModelForm):
    id_producto= forms.ModelChoiceField(queryset=Producto.objects.all(), label='Código del producto', widget=forms.TextInput, required=False)
    cantidad = forms.IntegerField(initial=1)

    class Meta:
        model = Compra
        fields = [
            'id_producto',
            'cantidad',
        ]