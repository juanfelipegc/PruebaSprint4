
from django.shortcuts import render


def base_layout(request):
    template = '../templates/base.html'
    return render(request, template)

def inicio(request):
    return render(request, "inicio.html", {})