from django.contrib import admin

# Register your models here.

from .models import Compra, Factura

admin.site.register(Compra)
admin.site.register(Factura)