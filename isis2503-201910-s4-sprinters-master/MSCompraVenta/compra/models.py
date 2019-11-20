from django.db import models
# Create your models here.

class Cliente(object):
    def __init__(self, c, n, e, p):
        self.cedula = c
        self.nombre = n
        self.email = e
        self.puntos = p

    def __str__(self):
        return str(self.cedula)

class Producto(object):
    def __init__(self, id, n, m, pr):
        self.id = id
        self.n = n
        self.m = m
        self.precio = pr

    def __str__(self):
        return self.nombre


class Factura(models.Model):
    id_cliente = models.CharField(max_length=32)
    fecha = models.DateField(null=True)
    metodo_pago = models.CharField(max_length=32, blank=True)
    envio_dian = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=1000, decimal_places=3,default=0)

    def __str__(self):
        return 'Factura: %s, Cliente: %s' % (self.id, self.id_cliente)

class Compra(models.Model):
    id_factura = models.ForeignKey(Factura, on_delete = models.CASCADE)
    id_producto = models.CharField(max_length=50)
    cantidad = models.IntegerField(default=1)
    preciofinal = models.DecimalField(max_digits=19, decimal_places=3, default=0.0, blank=True)

    class Meta:
        unique_together = (('id_factura', 'id_producto'),)
