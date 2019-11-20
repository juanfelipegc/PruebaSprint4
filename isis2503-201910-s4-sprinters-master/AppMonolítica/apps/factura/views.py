from django.shortcuts import render, get_object_or_404, get_list_or_404
from .forms import FacturaForm
from .models import Factura
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key
import datetime
import _thread
from ..compra.models import Compra
import requests
import hashlib
import json

from datetime import datetime

import xml.etree.ElementTree as ET

# From rest framework
from rest_framework import generics

# Create your views here.

def crearVistaFactura(request):
    form = FacturaForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = FacturaForm()
    context = {
        'form': form
    }
    return render(request, "factura/factura_create.html", context)

# Concretar Factura/Compra
def consolidarFactura(id):
    obj = get_object_or_404(Factura, id=id)
    client = obj.id_cliente
    compras_queryset = get_list_or_404(Compra, id_factura=obj.id)
    total = 0
    fecha = datetime.now()

    respuesta = imprimirFactura(total, compras_queryset, obj, client, fecha)
    xml = facturaXML(compras_queryset, obj, client, fecha)
    xml = xml.decode("utf-8")

    tupla = (xml,)
    _thread.start_new_thread(enviarDIAN,tupla)

    # mailcliente = client.email

    # email = EmailMessage(
    #     'Tu factura #'+obj.id,
    #     'Adjunto encuentra el resumen de su compra',
    #     from_email='ventas@atpos.com',
    #     to=[mailcliente]
    #  )

    # email.attach('factura.txt', respuesta)
    #email.send(fail_silently=False)

    obj.fecha = fecha
    obj.envio_dian = True
    obj.total = total
    obj.save()
    return respuesta

def enviarDIAN(textoEnviar):
    # certstr = requests.get('https://mock-server-dian.herokuapp.com/api/publickey')
    # print(certstr.text)
    # certDian = load_pem_public_key(certstr.text.encode(), backend=default_backend())
    dupla =  generarLlaves()
    pbk = dupla['c']
    prk = dupla['p']
    firmaPropia = firmar(textoEnviar, prk)

    # key = Fernet.generate_key()
    # f = Fernet(key)
    # encriptado = f.encrypt(bytes(textoEnviar.encode('ascii')))
    #
    # print(certDian.public_bytes(encoding=Encoding.PEM,format=PublicFormat.PKCS1))
    # llaveEncriptada = certDian.encrypt(
    #     key,
    #     padding.PKCS1v15()
    # )

    # print("llave: " + key.decode()

    envio = {}
    envio["xml"] = textoEnviar
    #envio["key"] = base64.b64encode(llaveEncriptada).decode()
    envio["firma"] = firmaPropia.hex()
    envio["certificado"] = pbk.public_bytes(encoding=Encoding.PEM,format=PublicFormat.SubjectPublicKeyInfo).decode()

    infoJson = json.dumps(envio, indent=0)

    r = requests.post('https://mock-server-dian.herokuapp.com/api/bills', data=infoJson, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    if r.status_code == 200:
        print("Info enviada y verificada correctamente.")

def firmar(texto, llaveprivada):
    hasheado = hashlib.sha256(texto.encode()).hexdigest()
    firma = llaveprivada.sign(
        hasheado.encode(),
        padding.PSS(
            mgf = padding.MGF1(hashes.SHA256()),
            salt_length = padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    # chosen_hash = hashes.SHA256()
    # hasher = hashes.Hash(chosen_hash, default_backend())
    # hasher.update(texto.encode())
    # digest = hasher.finalize()
    # sig = llaveprivada.sign(
    #     digest,
    #     padding.PKCS1v15(),
    #     utils.Prehashed(chosen_hash)
    # )
    return firma

def generarLlaves():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    retorno = {}
    retorno['c'] = public_key
    retorno['p'] = private_key
    return retorno

#XML FACTURA A LA DIAN
def facturaXML(compraQuery, factura, cliente, fecha):
    total = 0
    root = ET.Element('factura')
    root.set('id',str(factura.id))
    date = ET.SubElement(root, 'fecha')
    date.text = str(fecha)
    productoList = ET.SubElement(root, 'productoList')
    productoList.set('title','productos')
    for compra in compraQuery:
        prod = compra.id_producto
        producto = ET.SubElement(productoList, 'producto')

        nombre = ET.SubElement(producto, 'nombre')
        nombre.text = prod.nombre + "_" + prod.marca

        valorInd = ET.SubElement(producto, 'valorIndividual')
        valorInd.text = str(prod.precio)

        cantidad = ET.SubElement(producto, 'cantidad')
        cantidad.text = str(compra.cantidad)

        valorTotal = ET.SubElement(producto, 'valorTotal')
        val = compra.cantidad * prod.precio
        total += val
        valorTotal.text = str(val)
    subtotal = ET.SubElement(root, 'subtotal')
    subtotal.text = str(total)

    totalXML = ET.SubElement(root, 'total')
    totalXML.text = str(total*0.09)

    clienteXML = ET.SubElement(root, 'cliente')
    nombre = ET.SubElement(clienteXML, 'nombre')
    nombre.text = cliente.nombre

    cedula = ET.SubElement(clienteXML, 'cedula')
    cedula.text = str(cliente.cedula)
    factura = ET.tostring(root)
    return factura



#IMPRESION FACTURA
def imprimirFactura(total, compraQuery, factura, cliente, fecha):
    # NOMBRE SUCURSAL
    impresion = "ATPOS\n"

    # ADRESS SUCURSAL
    impresion = impresion + "Calle 19A No. 1 - 82 costado sur, Bogota (Colombia)\n"

    # FECHA Y HORA CONFIRMACION FACTURA
    impresion = impresion + str(fecha) + "\n"

    # COLUMNAS PRODUCTOS
    impresion = impresion + "NOMBRE\t\tCANTIDAD\t\tVALOR\n"

    # IMPRESION NOMBRE, CANTIDAD Y VALOR PRODUCTOS
    for compra in compraQuery:
        producto = compra.id_producto

        # NOMBRE Y MARCA PRODUCTO
        nombre = producto.nombre + " " + producto.marca

        # CANTIDAD COMPRADA PRODUCTO
        cantidad = str(compra.cantidad)

        # CALCULO VALOR TOTAL PRODUCTO
        valor = compra.cantidad * producto.precio
        total += valor

        impresion = impresion + nombre + "\t\t" + cantidad + "\t\t" + str(valor) + "\n"

    # SEPARADOR
    impresion = impresion + "----------------------------------------\n"

    # AGREGAR SUBTOTAL
    impresion = impresion + "SUBTOTAL = $" + str(total) + "\n"

    # SEPARADOR
    impresion = impresion + "----------------------------------------\n"

    # IMPUESTOS
    impresion = impresion + "MEDIO DE PAGO: " + str(factura.metodo_pago) + "\n"
    # ESTO ES TEMPORAL
    iva = 0.09
    impresion = impresion + "IVA: " + str(iva) + "\n"
    impuestos = total * iva
    impresion = impresion + "IMPUESTOS: " + str(impuestos) + "\n"
    impresion = impresion + "TOTAL: " + str(impuestos + total) + "\n"
    impresion = impresion + "----------------------------------------\n"
    if not cliente:
        impresion = impresion + "Pregunta en nuestras cajas para afiliarte!\n"
    else:
        cliente.puntos += (total/1000)
        cliente.save()
        impresion = impresion + "Cliente: " + cliente.nombre + "\n"
        impresion = impresion + "Cédula: " + str(cliente.cedula) + "\n"
    impresion = impresion + "----------------------------------------\n"
    impresion = impresion + "Para más información visitanos en:\n"
    impresion = impresion + "https://twitter.com/ATposMovil\n"
    impresion = impresion + "----------------------------------------\n"
    impresion = impresion + "ATPOS"
    return impresion