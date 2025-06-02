from django.db import models
import uuid
from apps.Clientes.models import Cliente
from apps.Productos.models import Producto

# Create your models here.
class Pedido(models.Model):
    choices = (
        ('Pendiente', 'Pendiente'),
        ('Entregado', 'Entregado'),
    )
    id_pedido = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='Pendiente', choices=choices)

    class Meta:
        db_table = 'Pedido'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return self.id_pedido
    
    