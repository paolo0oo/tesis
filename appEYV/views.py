from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Producto 
from .forms import CustomUserCreationForm, ProductoForm, TipoProductoForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.timezone import now, timezone

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def crearcuenta(request):
    return render(request, 'app/crearcuenta.html')

def pedido(request):
    return render(request, 'app/pedido.html')

def carrito(request):
    return render(request, 'app/carrito.html')

def pago(request):
    return render(request, 'app/pago.html')

def modificar_producto (request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect("listar-productos")
        data ["form"] = formulario
    return render(request, 'app/producto/modificar.html', data)

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        producto.delete()
        return HttpResponseRedirect(reverse('listar-productos')) 
    
    return render(request, 'app/producto/eliminar_confirmacion.html', {'producto': producto})

def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data ["mensaje"] = "Guardado correctamente"
        else:
            data ["form"] = formulario

    return render(request,'app/producto/agregar.html', data)



def agregar_tipo_prod(request):
    if request.method == 'POST':
        formulario = TipoProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save() 
            return redirect('listar-productos')  

    else:
        formulario = TipoProductoForm()

    return render(request, 'app/producto/agregar_tipo_prod.html', {'form': formulario})

def listar_productos(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
        
    
    return render (request, 'app/producto/listar.html', data)

def product_list(request):
    tipo = request.GET.get('tipo')  # Obtener el tipo de producto desde el parámetro de la URL
    if tipo:
        productos = Producto.objects.filter(Tipo_prod=tipo)  # Filtrar productos por tipo
    else:
        productos = Producto.objects.all()  # Obtener todos los productos si no se especifica tipo
    
    paginator = Paginator(productos, 12)  # Mostrar 12 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/home.html', {'page_obj': page_obj, 'tipo': tipo})
# def product_list(request):
#     productos = Producto.objects.all()  
#     paginator = Paginator(productos, 12) 
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'app/home.html', {'page_obj': page_obj})


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario=CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Registro Correcto")
            return redirect(to="product_list")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def productos(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'productos.html', {'products': productos})

@csrf_exempt
def carrito(request):
    if request.method == 'POST':
        cart = json.loads(request.body)  # Puede fallar si el JSON está malformado
        # Aquí puedes procesar los datos y luego redirigir o renderizar
        return JsonResponse({'success': True, 'message': 'Carrito procesado'})
    else:
        # Renderiza la página del carrito
        cart = request.session.get('cart', {})
        total = sum(item['Precio'] * item['cantidad'] for item in cart.values())
        return render(request, 'app/carrito.html', {'cart': cart, 'total': total})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Pago

@csrf_exempt
def procesar_pago(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            # Generar el ID de pago si no se proporciona
            id_pago = get_random_string(length=10)  # Genera un ID de pago aleatorio
            
            # Obtener la fecha y hora actual para el comprobante
            fecha_hora_actual = timezone.now().strftime('%Y%m%d-%H%M%S')
            comprobante = f"COMP-{fecha_hora_actual}"

            # Obtener el carrito de la sesión
            cart = request.session.get('cart', {})

            # Asumimos que solo se está comprando un producto por ahora, así que tomamos el primer producto
            id_producto = list(cart.keys())[0]  # Esto toma el primer producto en el carrito (puedes adaptarlo si es necesario)

            # Crear la venta
            Venta.objects.create(
                TipoVenta="Venta Online",  # Puedes cambiarlo según tu necesidad
                Fecha=timezone.now().date(),
                Comprobante=comprobante,
                DetalleVenta="Detalles de la compra",  # Agrega detalles de la venta aquí
                ID_pago=id_pago,
                ID_producto=id_producto,
                ID_Factura=None,  # Si no hay factura aún
                ID_mediopago="PayPal",  # O el medio de pago que corresponde
            )

            return JsonResponse({'success': True, 'comprobante': comprobante, 'id_pago': id_pago})

        except Exception as e:
            print(f"Error al procesar el pago: {e}")
            return JsonResponse({'success': False, 'error': str(e)})

    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
@csrf_exempt
def guardar_carrito(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            cart = datos['cart']  # Recibe el carrito del frontend

            # Guardar el carrito en la sesión
            request.session['cart'] = cart  # Guardamos el carrito completo en la sesión
            request.session['cart_total'] = datos['total']  # Guarda el total en la sesión

            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error al guardar el carrito: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
    
from transbank.webpay.webpay_plus.transaction import Transaction

# Vista para iniciar pago con Transbank
def iniciar_pago_transbank(request):
    total = request.session.get('cart_total', 0)

    # Crear una nueva instancia de Venta
    nueva_venta = Venta.objects.create(
        TipoVenta="Online",  # Cambia según tu lógica de negocio
        Fecha=now().date(),
        Comprobante="N/A",  # Este campo se completará después del pago
        DetalleVenta="Descripción del pedido",  # Cambia esto según sea necesario
        ID_pago=0,  # Se actualizará después del pago
        ID_producto=0,  # Se puede actualizar más tarde según sea necesario
        ID_Factura="Pendiente",  # Completar después del pago
        ID_mediopago=0,  # Cambiar con el método de pago real
    )

    transaction = Transaction()
    response = transaction.create(
        buy_order=f"orden_{nueva_venta.id}",  # Usa el ID de la venta como parte del identificador único
        session_id=str(nueva_venta.id),  # Usa el ID de la venta como sesión
        amount=total,
        return_url="http://127.0.0.1:8000/resultado-transbank/"
    )

    # Puedes almacenar el ID de la venta en la sesión para actualizarlo luego
    request.session['venta_id'] = nueva_venta.id

    return redirect(response['url'] + '?token_ws=' + response['token'])

def pago(request):
    total = request.session.get('cart_total', 0)  # Obtén el total desde la sesión
    context = {
        'total': total
    }
    return render(request, 'app/pago.html', context)

from transbank.webpay.webpay_plus.transaction import Transaction
from .models import Venta


def resultado_transbank(request):
    token_ws = request.GET.get('token_ws')
    transaction = Transaction()
    response = transaction.commit(token_ws)

    # Obtén el ID de la venta almacenada en la sesión
    venta_id = request.session.get('venta_id')
    venta = get_object_or_404(Venta, id=venta_id)

    # Actualiza la venta con los datos de Transbank
    venta.Comprobante = response.get('buy_order', 'N/A')  # Orden de compra
    venta.ID_pago = response.get('transaction_id', 0)  # ID del pago
    venta.Fecha = now().date()  # Fecha actual de la transacción

    # DetalleVenta, TipoVenta, y otros datos adicionales
    venta.DetalleVenta = f"Pago de {response.get('amount', 0)} CLP"
    venta.TipoVenta = "WebPay"  # Asumiendo que la venta es por WebPay
    venta.ID_producto = 0.0  # Si no tienes un producto asociado, usar un valor por defecto
    venta.save()

    context = {
        'venta': venta,
        'response': response,
    }

    return render(request, 'app/resultado_transbank.html', context)