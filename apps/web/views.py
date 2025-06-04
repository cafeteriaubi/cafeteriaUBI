import json
import uuid
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from apps.Productos.models import Producto, Categoria
from apps.Clientes.models import Cliente
from apps.Ventas.models import Ventas, DetalleVenta

def index(request):
    """Vista principal que muestra la página de la cafetería"""
    productos = Producto.objects.filter(disponible=True).select_related('categoria')
    categorias = Categoria.objects.all()
    
    context = {
        'productos': productos,
        'categorias': categorias,
    }
    return render(request, 'index.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def crear_pedido(request):
    """Vista para crear un pedido y mostrar datos bancarios"""
    try:
        data = json.loads(request.body)
        cart_items = data.get('cart_items', [])
        cliente_id = data.get('cliente_id')
        
        if not cart_items:
            return JsonResponse({'error': 'El carrito está vacío'}, status=400)
        
        # Obtener o crear cliente (por ahora usamos uno por defecto)
        try:
            cliente = Cliente.objects.get(id_cliente=cliente_id) if cliente_id else None
        except Cliente.DoesNotExist:
            cliente = None
            
        if not cliente:
            # Crear cliente temporal o usar uno por defecto
            cliente, created = Cliente.objects.get_or_create(
                correo='cliente@temporal.com',
                defaults={
                    'nombre': 'Cliente',
                    'apellido': 'Temporal',
                }
            )
        
        # Calcular total
        total = Decimal('0.00')
        productos_pedido = []
        
        for item in cart_items:
            try:
                producto = Producto.objects.get(id_producto=item['id'])
                cantidad = int(item['quantity'])
                subtotal = producto.precio * cantidad
                total += subtotal
                
                productos_pedido.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'subtotal': subtotal
                })
            except Producto.DoesNotExist:
                return JsonResponse({'error': f'Producto {item["id"]} no encontrado'}, status=400)
        
        # Crear la venta
        venta = Ventas.objects.create(
            cliente=cliente,
            total=total
        )
        
        # Crear los detalles de venta
        for item in productos_pedido:
            # Crear el detalle de venta con el producto directamente
            DetalleVenta.objects.create(
                venta=venta,
                producto=item['producto'],
                cantidad=item['cantidad'],
                subTotal=item['subtotal']
            )
        
        # Usar imagen fija de cuenta bancaria
        cuenta_bancaria_url = "/static/images/cuenta_bancaria.jpg"
        
        return JsonResponse({
            'success': True,
            'venta_id': str(venta.id_venta),
            'total': float(total),
            'qr_image_url': cuenta_bancaria_url,  # Cambié el nombre para que coincida con el JS
            'message': 'Pedido creado exitosamente'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def confirmar_pago(request):
    """Vista para confirmar el pago y finalizar el pedido"""
    try:
        data = json.loads(request.body)
        venta_id = data.get('venta_id')
        
        if not venta_id:
            return JsonResponse({'error': 'ID de venta requerido'}, status=400)
        
        try:
            venta = Ventas.objects.get(id_venta=venta_id)
            
            # Aquí podrías agregar lógica adicional para marcar como pagado
            # Por ejemplo, agregar un campo 'pagado' al modelo Ventas
            
            return JsonResponse({
                'success': True,
                'message': 'Pago confirmado exitosamente. Tu pedido está siendo procesado.',
                'venta_id': str(venta.id_venta)
            })
            
        except Ventas.DoesNotExist:
            return JsonResponse({'error': 'Venta no encontrada'}, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def obtener_productos(request):
    """API para obtener todos los productos disponibles"""
    productos = Producto.objects.filter(disponible=True).select_related('categoria')
    
    productos_data = []
    for producto in productos:
        productos_data.append({
            'id': str(producto.id_producto),
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': float(producto.precio),
            'imagen': producto.url_imagen,
            'categoria': producto.categoria.nombre,
            'disponible': producto.disponible
        })
    
    return JsonResponse({
        'productos': productos_data
    })

class HistorialVentasView(View):
    """Vista para mostrar el historial de ventas"""
    def get(self, request):
        ventas = Ventas.objects.all().select_related('cliente').prefetch_related('detalles__producto')
        
        context = {
            'ventas': ventas
        }
        return render(request, 'cafeteria/historial_ventas.html', context)
