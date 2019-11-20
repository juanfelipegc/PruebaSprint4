from django import forms
from .models import Factura
from ..cliente.models import Cliente

class FacturaForm(forms.ModelForm):
    id_cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())

    metodo_pago = forms.CharField(label='',
                           widget=forms.TextInput(attrs={"placeholder": "Payment method"}))

    class Meta:
        model = Factura
        fields = [
            'id_cliente',
            'metodo_pago'
        ]