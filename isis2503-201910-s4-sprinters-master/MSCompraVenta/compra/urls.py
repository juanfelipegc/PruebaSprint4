from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'factura', views.FacturaView)
router.register(r'compra', views.CompraView)

urlpatterns = [
    path('', include(router.urls))
]