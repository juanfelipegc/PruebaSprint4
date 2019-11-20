from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
import json
from .models import Factura, Compra, Cliente, Producto
from .serializers import FacturaSerial,CompraSerial
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Factura
from django.http import Http404
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key
import datetime
import _thread
import requests
import hashlib
import json

from datetime import datetime

import xml.etree.ElementTree as ET

from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError




def obtenerCliente(cedula):
    a = {}
    a["cedula"] = cedula
    b = {}
    b["TableName"] = "Clientes"
    b["Key"] = a
    env = json.dumps(b)
    a = requests.get('https://5r3kozjj10.execute-api.us-west-1.amazonaws.com/test/clientes?TableName=Clientes',data=env)
    try:
        rta = a.json()["Item"]
        cli = Cliente(rta["cedula"], rta["nombre"], rta["email"], int(rta["puntos"]))
        return cli
    except:
        raise Http404

def enviarPuntos(idcl, pnts):
    a = {}
    a["cedula"] = idcl
    b = {}
    b["TableName"] = "Clientes"
    b["Key"] = a
    b["UpdateExpression"] = "set puntos = puntos + :p"
    b["ExpressionAttributeValues"] = {":p":pnts}

def enviarKafka(compraQuery):
    prod = KafkaProducer(bootstrap_servers=["ec2-52-90-84-251.compute-1.amazonaws.com:9092"])
    for compra in compraQuery:
        a = {"codigoBarras":compra.id_producto,"comprados":compra.cantidad}
        b = json.dumps(a)
        try:
            prod.send("actualizaciones", str.encode(b))
        except:
            print("err")
    prod.flush()

def consolidarFactura(id):
    obj = get_object_or_404(Factura, id=id)
    client = obtenerCliente(obj.id_cliente)
    compras_queryset = get_list_or_404(Compra, id_factura=obj.id)
    total = 0
    fecha = datetime.now()

    respuesta = imprimirFactura(total, compras_queryset, obj, client, fecha)
    enviarKafka(compras_queryset)
    if client:
        xml = facturaXML(compras_queryset, obj, client, fecha)
        xml = xml.decode("utf-8")
        enviarPuntos(client.cedula, len(compras_queryset)*5)
        tupla = (xml,)
        _thread.start_new_thread(enviarDIAN, tupla)

    obj.fecha = fecha
    obj.envio_dian = True
    obj.total = float(total)
    obj.save()
    return respuesta

def generarLlaves():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    retorno = {}
    retorno['c'] = public_key
    retorno['p'] = private_key
    return retorno

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
    return firma

def enviarDIAN(textoEnviar):
    dupla =  generarLlaves()
    pbk = dupla['c']
    prk = dupla['p']
    firmaPropia = firmar(textoEnviar, prk)

    envio = {}
    envio["xml"] = textoEnviar
    envio["firma"] = firmaPropia.hex()
    envio["certificado"] = pbk.public_bytes(encoding=Encoding.PEM,format=PublicFormat.SubjectPublicKeyInfo).decode()

    infoJson = json.dumps(envio, indent=0)

    requests.post('https://mock-server-dian.herokuapp.com/api/bills', data=infoJson, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})


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
        producto = enviarProductos(compra.id_producto,-1)

        # NOMBRE Y MARCA PRODUCTO
        nombre = producto.n + " " + producto.m

        # CANTIDAD COMPRADA PRODUCTO
        cantidad = str(compra.cantidad)

        # CALCULO VALOR TOTAL PRODUCTO
        total += compra.preciofinal

        impresion = impresion + nombre + "\t\t" + cantidad + "\t\t" + str(compra.preciofinal) + "\n"

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
    impuestos = float(total) * iva
    impresion = impresion + "IMPUESTOS: " + str(impuestos) + "\n"
    impresion = impresion + "TOTAL: " + str(impuestos) + str(total) + "\n"
    impresion = impresion + "----------------------------------------\n"
    if not cliente:
        impresion = impresion + "Pregunta en nuestras cajas para afiliarte!\n"
    else:
        impresion = impresion + "Cliente: " + cliente.nombre + "\n"
        impresion = impresion + "Cédula: " + str(cliente.cedula) + "\n"
    impresion = impresion + "----------------------------------------\n"
    impresion = impresion + "Para más información visitanos en:\n"
    impresion = impresion + "https://twitter.com/ATposMovil\n"
    impresion = impresion + "----------------------------------------\n"
    impresion = impresion + "ATPOS"
    return impresion

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
        prod = enviarProductos(compra.id_producto,-1)
        producto = ET.SubElement(productoList, 'producto')

        nombre = ET.SubElement(producto, 'nombre')
        nombre.text = prod.n + "_" + prod.m

        valorInd = ET.SubElement(producto, 'valorIndividual')
        valorInd.text = str(prod.precio)

        cantidad = ET.SubElement(producto, 'cantidad')
        cantidad.text = str(compra.cantidad)

        valorTotal = ET.SubElement(producto, 'valorTotal')
        total+=compra.preciofinal
        valorTotal.text = str(compra.preciofinal)
    subtotal = ET.SubElement(root, 'subtotal')
    subtotal.text = str(total)

    totalXML = ET.SubElement(root, 'total')
    totalXML.text = str(float(total)*0.09)

    clienteXML = ET.SubElement(root, 'cliente')
    nombre = ET.SubElement(clienteXML, 'nombre')
    nombre.text = cliente.nombre

    cedula = ET.SubElement(clienteXML, 'cedula')
    cedula.text = str(cliente.cedula)
    factura = ET.tostring(root)
    return factura

class FacturaView(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerial

    def create(self, request):
        context = {
            'request': request,
        }
        a = request.data
        obtenerCliente(a["id_cliente"])
        serializer = FacturaSerial(data=a,context=context)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request,pk):
        factura = consolidarFactura(pk)
        factura = factura.replace("\t", "&#9;")
        factura = factura.replace("\n", "<br>")
        return Response({"factura":factura})




class CompraView(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerial

    def create(self, request):
        self.request.POST._mutable = True
        a = request.data
        a["preciofinal"] = 0.00
        a["cantidad"] = int(a["cantidad"])
        a["id_factura"] = int(a["id_factura"])
        context = {
            'request': request,
        }
        get_object_or_404(Factura, id=a["id_factura"])
        prod = enviarProductos(a["id_producto"], a["cantidad"])
        print(a)
        compra = CompraSerial(data=a,context=context)
        if compra.is_valid():
            print("hola")
            cant = request.data["cantidad"]
            compra.preciofinal = cant*prod.precio
            compra.save()
            return Response(compra.data)


def enviarProductos(codigo, cantidad):
    a = requests.get("http://54.173.226.195:8000/inventario/productos/%s" % codigo)
    b = a.json()
    if int(b["existencias"]) >= int(cantidad):
        prod = Producto(b["codigoBarras"], b["nombre"], b["marca"],b["precio"])
        return prod
    else:
        raise APIException("No hay existencias")