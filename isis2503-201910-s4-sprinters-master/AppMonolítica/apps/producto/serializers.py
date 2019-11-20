from rest_framework import serializers
from .models import Producto


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ("id", "nombre", "marca", "precio")