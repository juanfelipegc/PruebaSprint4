from rest_framework import serializers
from .models import Factura,Compra



class FacturaSerial(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ('url','id', 'id_cliente', 'fecha', 'metodo_pago', 'envio_dian', 'total')

class CompraSerial(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ('url', 'id_factura', 'id_producto', 'cantidad')