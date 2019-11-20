from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm, idForm
from .models import Producto
from django.contrib.auth.decorators import login_required
from ..login.views import getRole
from django.http import HttpResponseRedirect, HttpResponse
import hashlib

# From rest framework
from rest_framework import generics
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie


@login_required
def crearVistaProducto(request):
    role = getRole(request)
    if role == "admin":
        form = ProductForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = ProductForm()
        context = {
            'form': form
        }
        return render(request, "producto/product_create.html", context)
    else:
        return HttpResponse("Unauthorized User")

@login_required
def searchForUpdate(request):
    role = getRole(request)
    if role == 'admin':
        if request.method == 'POST' and 'searchUpdate' in request.POST:
            search_id = request.POST.get('textfield', None)
            try:
                producto = Producto.objects.get(id=search_id)
                form = ProductForm(request.POST or None, instance=producto)
                if form.is_valid():
                    form.save()
                context = {
                    'form': form
                }
                return render(request, "producto/product_update.html", context)
            except Producto.DoesNotExist:
                return HttpResponse("El producto no existe")
        else:
            return render(request, 'producto/product_update.html')
    else:
        return HttpResponse("Unauthorized User")

@login_required
def updateViewProducto(request):
    role = getRole(request)
    if role == 'admin':
        return render(request, 'producto/product_update.html')
    else:
        return HttpResponse("Unauthorized User")

@login_required
def getProduct(request, id_producto, iObjeto):
    obj = get_object_or_404(Producto, id=id_producto)
    form = ProductForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "producto/product_update.html", context)


@login_required
def detailViewProducto(request, id):
    obj = get_object_or_404(Producto, id=id)
    context = {
        "object": obj
    }
    return render(request, "producto/product_detail.html", context)


@login_required
def deleteViewProducto(request, id):
    role = getRole(request)
    if role == "admin":
        obj = get_object_or_404(Producto, id=id)
        if request.method == "POST":
            obj.delete()
            return redirect('../../')
        context = {
            "object": obj
        }
        return render(request, "producto/product_delete.html", context)
    else:
        return HttpResponse("Unauthorized User")


# Rest framework
class GetProducto(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        id = self.kwargs['id']
        return Producto.objects.filter(id=id)
