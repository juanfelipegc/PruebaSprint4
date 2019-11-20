from django.db import models

# Create your models here.
class Cliente(models.Model):
    cedula = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=32)
    email = models.EmailField()
    puntos = models.BigIntegerField()

    def __str__(self):
        return str(self.cedula)



