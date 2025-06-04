from django.shortcuts import render
from apps.Productos.models import Categoria, Producto

def index(request):
    categorias = Categoria.objects.all()
    
    productos_por_categoria = {
        categoria: list(filter(lambda p: p.categoria == categoria, Producto.objects.all()))
        for categoria in categorias
    }

    context = {
        'categorias': categorias,
        'productos_por_categoria': productos_por_categoria,
    }
    return render(request, "index.html", context)
