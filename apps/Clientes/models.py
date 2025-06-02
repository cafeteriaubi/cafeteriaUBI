import uuid
from django.db import models

# Create your models here.
class Cliente(models.Model):
    id_cliente=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=200)
    correo=models.EmailField(max_length=254) 
    avatar=models.URLField(null=True)
    class Meta:
        db_table="clientes"
        verbose_name="Cliente"
        verbose_name_plural="Clientes"
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    