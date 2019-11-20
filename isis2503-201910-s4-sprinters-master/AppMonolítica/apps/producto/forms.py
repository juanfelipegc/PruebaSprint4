from django import forms

from .models import Producto


class ProductForm(forms.ModelForm):
    id = forms.CharField(label='',
                           widget=forms.TextInput(attrs={"placeholder": "ID del producto"}))
    nombre = forms.CharField(label='',
                           widget=forms.TextInput(attrs={"placeholder": "Nombre del producto"}))
    marca = forms.CharField(label='',
                            widget=forms.TextInput(attrs={"placeholder": "Marca del producto"}))
    precio = forms.DecimalField(initial=0.0)

    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'marca',
            'precio'
        ]


class RawProductForm(forms.Form):
    nombre = forms.CharField(label='',
                           widget=forms.TextInput(attrs={"placeholder": "Product nombre"}))
    marca = forms.CharField(label='',
                            widget=forms.TextInput(attrs={"placeholder": "Product marca"}))
    precio = forms.DecimalField(initial=0.0)

class idForm(forms.Form):
    id = forms.CharField(label='',
                             widget=forms.TextInput(attrs={"placeholder": "ID del producto"}))
