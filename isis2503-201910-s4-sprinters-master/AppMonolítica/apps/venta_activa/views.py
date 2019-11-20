from django.shortcuts import render, get_object_or_404, redirect

from ..factura.models import Factura
from ..factura.views import consolidarFactura
from ..cliente.models import Cliente
from .forms import VentaActivaForm
from ..compra.forms import CompraForm
from random import randint


# from datetime import datetime

# Create your views here.

def crearVistaVentaActiva(request):
    # QUIERO ACA CREAR UNA FACTURA CON LA INFO POR DEFAULT Y PASARSELA
    # AL CONTEXTO PARA QUE ALLÍ COMO QUE SE TENGA EL ID O ALGO.
    # QUIERO CREAR TAMBIEN EL CLIENTE O AÑADIRLO SI DA SUS DATOS!!!
    if request.method == 'POST':
        form = VentaActivaForm(request.POST or None)
        if form.is_valid():
            cliente = Cliente.objects.get(cedula=form['id_cliente'].value())

            facturanueva = Factura(id_cliente=cliente, id=randint(1, 1001), fecha=None, metodo_pago='EFECTIVO',
                                   envio_dian=False, total=0)
            facturanueva.save()

            activa = form.save(commit=False)
            activa.id_factura = facturanueva
            activa.save()

            return redirect("venta_activa:vender-productos", facturacion=facturanueva)
    else:
        form = VentaActivaForm()
    context = {
        'form': form,
    }
    return render(request, "venta_activa/inicio.html", context)


def venderProductos(request, facturacion):
    if request.method == 'POST':
        if request.POST.get("fin"):
            return redirect("venta_activa:terminar-venta", facturacion=facturacion)

        obj = get_object_or_404(Factura, id=facturacion)
        form = CompraForm(request.POST or None)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.id_factura = obj
            compra.save()
            form = CompraForm()
    else:
        form = CompraForm()
    context = {
        'compra': form,
    }

    return render(request, "venta_activa/venta_activa.html", context)


def terminar(request, facturacion):
    factura = consolidarFactura(facturacion)
    factura = factura.replace("\t","&#9;")
    factura = factura.replace("\n", "<br>")
    consolidado = "<pre>" + factura + "</pre>"
    context = {
        'factura': consolidado
    }
    return render(request, "venta_activa/bye.html", context)
