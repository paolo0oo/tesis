from django.contrib import admin
from .models import Venta, Administrador, Usuario, Producto, DetalleVenta, Factura, Pago, Cliente, Compra, MedioPago, TipoProducto
# Register your models here.

admin.site.register(Venta)
admin.site.register(Administrador)
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(DetalleVenta)
admin.site.register(Factura)
admin.site.register(Pago)
admin.site.register(Cliente)
admin.site.register(Compra)
admin.site.register(MedioPago)
admin.site.register(TipoProducto)