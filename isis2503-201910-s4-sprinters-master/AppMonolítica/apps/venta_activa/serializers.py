from rest_framework import serializers
from ..factura.models import Factura

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ("id_cliente", "id", "fecha", "metodo_pago", "envio_dian", "total")