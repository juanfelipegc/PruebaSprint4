from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    crearVistaVentaActiva,
    venderProductos,
    terminar
)

app_name = 'venta_activa'
urlpatterns = [
    path('', crearVistaVentaActiva, name='venta-activa'),
    path('vender/<facturacion>/', csrf_exempt(venderProductos), name='vender-productos'),
    path('terminar/<facturacion>/', csrf_exempt(terminar), name='terminar-venta'),
]