from django.urls import path, include
from .views import home, crearcuenta, pedido, product_list, registro, agregar_producto, listar_productos,modificar_producto, eliminar_producto
from django.contrib import admin
from . import views


urlpatterns = [
    # path('', home, name="home"),
    path('crearcuenta/', crearcuenta, name="crearcuenta"),
    path('pedido.html/', pedido, name="pedido"),
    path('', product_list, name="product_list"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', registro, name="registro"),
    path('agregar-producto/', agregar_producto, name="agregar-producto"),
    path('listar-producto/', listar_productos, name="listar-productos"),
    path('modificar-producto/<str:id>/', modificar_producto, name="modificar-producto"),
    path('carrito/', views.carrito, name='carrito'),
    path('pago/', views.pago, name='pago'),
    path('agregar-tipo-prod/', views.agregar_tipo_prod, name='agregar-tipo-prod'),
    path('eliminar-producto/<str:id>/', views.eliminar_producto, name='eliminar-producto'),
    path('guardar-carrito/', views.guardar_carrito, name='guardar_carrito'),
    path('iniciar-pago-transbank/', views.iniciar_pago_transbank, name='iniciar_pago_transbank'),
]
# urls.py (principal del proyecto)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

