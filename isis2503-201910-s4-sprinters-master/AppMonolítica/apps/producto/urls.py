from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import (
    crearVistaProducto,
    detailViewProducto,
    deleteViewProducto,
    updateViewProducto,
    GetProducto,
    searchForUpdate
)
from . import views

app_name = 'producto'
urlpatterns = [
    path('', updateViewProducto, name='producto-create'),
    path('create/', crearVistaProducto, name='producto-create'),
    path('<str:id>/', detailViewProducto, name='producto-detail'),
    path('update/', updateViewProducto, name='producto-update'),
    path('<str:id>/delete/', deleteViewProducto, name='producto-delete'),
    path('get/<str:id>', GetProducto.as_view(), name='producto-get-rest'),
    path('upp', updateViewProducto, name='upp'),
    path('searchUpdate', searchForUpdate)
]