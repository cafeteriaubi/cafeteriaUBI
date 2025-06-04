from django.urls import path
from .views import index, crear_pedido, confirmar_pago, obtener_productos, HistorialVentasView
urlpatterns = [
    path('', index, name='index'),
    path('crear-pedido/', crear_pedido, name='crear_pedido'),
    path('confirmar-pago/', confirmar_pago, name='confirmar_pago'),
    path('api/productos/', obtener_productos, name='obtener_productos'),
    path('historial-ventas/', HistorialVentasView.as_view(), name='historial_ventas'),
]