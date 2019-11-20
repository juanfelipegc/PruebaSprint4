from django.db import models

# Create your models here.

class VentaActiva(models.Model):
    id_factura = models.ForeignKey('factura.Factura', on_delete = models.CASCADE)
    id_cliente = models.ForeignKey('cliente.Cliente', on_delete = models.CASCADE)

    def __str__(self):
        return 'Factura: %s, Cliente: %s' % (self.id_factura, self.id_cliente)