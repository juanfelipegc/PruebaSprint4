from django.db import models

# Create your models here.

class Compra(models.Model):
    id_factura = models.ForeignKey('factura.Factura',
                                on_delete = models.CASCADE,
                                )
    id_producto = models.ForeignKey('producto.Producto',
                                   on_delete = models.CASCADE, )
    cantidad = models.IntegerField(default=1)