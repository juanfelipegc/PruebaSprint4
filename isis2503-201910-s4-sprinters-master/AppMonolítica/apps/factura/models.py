from django.db import models

# Create your models here.

class Factura(models.Model):

    id_cliente = models.ForeignKey('cliente.Cliente', on_delete = models.CASCADE, null=True)
    id = models.BigIntegerField(primary_key=True, unique=True)
    fecha = models.DateField(null=True)
    metodo_pago = models.CharField(max_length=32, null=True)
    envio_dian = models.BooleanField()
    total = models.DecimalField(max_digits=1000, decimal_places=3)

    def __str__(self):
        return str(self.id)