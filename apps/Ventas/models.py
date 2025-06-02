from django.db import models
import uuid
from django.utils.timezone import now
from apps.Clientes.models import Cliente
from apps.Productos.models import Producto

class Ventas(models.Model):
    id_venta=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    fecha_venta=models.DateField(auto_now_add=True,null=True)
    total=models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # comprobante=models.CharField()
    class Meta:
        db_table="Venta"
    def __str__(self):
        return self.total
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.producto.precio
        super().save(*args, **kwargs)
        self.venta.calcular_total()  # Actualiza el total de la venta cada vez que se guarda un detalle.

class DetalleVenta(models.Model):
    id_detalle_venta=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE, related_name="detalles")
    cantidad=models.PositiveIntegerField()
    producto = models.ManyToManyField(Producto)
    subTotal=models.DecimalField(max_digits=10, decimal_places=2)
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.producto.precio
        super().save(*args, **kwargs)
    class Meta:
        db_table="DetalleVenta"
    def __str__(self):
        return self.cantidad+self.producto.nombre
    
# class Comprobante(models.Model):
#     id_comprobante=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
#     venta = models.OneToOneField(Ventas, on_delete=models.CASCADE, related_name="comprobante")
#     numero_comprobante = models.IntegerField()  # Número de factura o comprobante
#     # archivo = models.FileField(upload_to="comprobantes/", blank=True, null=True)  # Archivo opcional
#     fecha_emision = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Comprobante {self.numero} - Venta {self.venta.id}"
# Create your models here.
