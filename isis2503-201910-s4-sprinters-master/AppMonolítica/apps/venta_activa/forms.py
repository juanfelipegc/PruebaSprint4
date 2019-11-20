from django import forms

from .models import VentaActiva
from ..cliente.models import Cliente


class VentaActivaForm(forms.ModelForm):
    id_cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Ingrese la cédula del cliente', widget=forms.TextInput, required=False,)


    class Meta:
        model = VentaActiva
        fields = [
            'id_cliente'
        ]