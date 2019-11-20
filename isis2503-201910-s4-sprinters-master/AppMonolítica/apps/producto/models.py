from django.db import models

# Create your models here.

class Producto(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    nombre = models.CharField(max_length=32)
    marca = models.CharField(max_length=32)
    precio = models.BigIntegerField()

    def __str__(self):
        return self.nombre


