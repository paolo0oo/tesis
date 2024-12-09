from django.db import models

# Create your models here.

class Venta(models.Model):
    TipoVenta = models.CharField(max_length=30)
    Fecha = models.DateField()
    Comprobante = models.CharField(max_length=30)

    DetalleVenta = models.CharField(max_length=255)
    ID_pago = models.IntegerField()
    ID_producto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ID_Factura = models.CharField(max_length=30, null=True, blank=True)
    ID_mediopago = models.CharField(max_length=30)
    def __str__(self):
        return self.Comprobante
    
class Administrador(models.Model):
    ID_admin = models.CharField(max_length=3)
    Nombre_admn = models.CharField(max_length=20)
    Apellido_admn = models.CharField(max_length=20)
    ID_admin = models.IntegerField()

    def __str__(self):
        return self.ID_admin
    
class Usuario(models.Model):
    ID_usuario = models.CharField(max_length=3)
    Nombre_usr = models.CharField(max_length=30)
    Apellido_usr = models.CharField(max_length=30)
    Tipo_usr = models.CharField(max_length=30)

    def __str__(self):
        return self.ID_usuario
tipo_prod = (
    (0,"Linterna"),
    (1,"Herramienta")
)

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    ID_prod = models.CharField(max_length=3, unique=True, editable=False)
    Tipo_prod = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    Precio = models.IntegerField()
    nombre_prod = models.CharField(max_length=50, default='Producto Genérico')
    Imagen = models.ImageField(upload_to='img/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.ID_prod:  # Si no tiene ID_prod asignado
            last_product = Producto.objects.all().order_by('ID_prod').last()
            if last_product:
                last_id = int(last_product.ID_prod) + 1
            else:
                last_id = 1
            self.ID_prod = str(last_id).zfill(3)
        super(Producto, self).save(*args, **kwargs)

    def __str__(self):
        return self.ID_prod

class DetalleVenta(models.Model):
    TipoComprobante = models.CharField(max_length=20)
    SerieComprobante = models.CharField(max_length=7)
    NumComprobante = models.CharField(max_length=8)
    fecha_hora = models.DateTimeField
    impuesto = models.IntegerField()
    total_venta = models.IntegerField()
    estado = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.estado} - {'Completada' if self.estado else 'Pendiente'}"
    def __str__(self):
        return self.NumComprobante

class Factura(models.Model):
    ID_factura = models.CharField(max_length=3)
    Fecha_emision = models.DateField()
    Ciudad = models.CharField(max_length=30)
    Giro = models.CharField(max_length=30)
    Monto = models.IntegerField()

    def __str__(self):
        return self.ID_factura

class Pago(models.Model):
    ID_pago = models.CharField(max_length=3)
    Tipo_pago = models.CharField(max_length=30)
    ID_compra = models.IntegerField()

    def __str__(self):
        return self.ID_pago
    
class Cliente(models.Model):
    ID_cliente = models.CharField(max_length=3)
    Nombre_cli = models.CharField(max_length=30)
    Apellido_cli = models.CharField(max_length=30)
    ID_usuario = models.IntegerField()

    def __str__(self):
        return self.ID_cliente

class Compra(models.Model):
    ID_compra = models.CharField(max_length=3)
    ID_cliente = models.IntegerField()
    ID_pago = models.IntegerField()
    
    def __str__(self):
        return self.ID_compra
    
class MedioPago(models.Model):
    Tipo_pago = models.CharField(max_length=20)
    ID_pago = models.CharField(max_length=3)

    def __str__(self):
        return self.ID_pago