from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from SISTEMA.utils.utils import validar_rut



class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse("rol_detail", kwargs={"pk": self.pk})
    

    
class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse("tipoproducto_detail", kwargs={"pk": self.pk})
    


class MetodoContacto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse("metodocontacto_detail", kwargs={"pk": self.pk})
    
    

class MetodoPago(models.Model):
    
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse("metodopago_detail", kwargs={"pk": self.pk})
    
    
class TipoCliente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse("tipocliente_detail", kwargs={"pk": self.pk})
    


class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    nombre_comercio = models.CharField(max_length=150, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    ubicacion = models.CharField(max_length=255, null=True, blank=True)
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.CASCADE, null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"
    
    def get_absolute_url(self):
        return reverse("cliente_detail", kwargs={"pk": self.pk})
    
    
    
class Usuario(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=True)
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    
    def __str__(self):
        return f"{self.username} ({self.rut})"
    
    def get_absolute_url(self):
        return reverse("usuario_detail", kwargs={"pk": self.pk})
    
    

class PosibleCliente(models.Model):
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True, validators=[validar_rut])
    nombre_comercio = models.CharField(max_length=150, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(null=True, blank=True)
    ubicacion = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"
    
    def get_absolute_url(self):
        return reverse("Posible_cliente_detail", kwargs={"pk": self.pk})
    

class ListaTiposProducto(models.Model):
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.tipo_producto.nombre
    
    def get_absolute_url(self):
        return reverse("listatiposproducto_detail", kwargs={"pk": self.pk})
    
    
class InformeVendedor (models.Model):
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    venta_realizada = models.BooleanField(default=False)
    tipo_producto = models.ManyToManyField(TipoProducto, blank=True)
    descripcion = models.TextField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_termino = models.DateTimeField(null=True, blank=True)
    metodo_contacto = models.ForeignKey(MetodoContacto, on_delete=models.CASCADE, null=True, blank=True)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, null=True, blank=True)
    
    
    def __str__(self):
        return f"Informe de {self.vendedor.username} - {self.fecha_ingreso.strftime('%Y-%m-%d')}"
    
    def get_absolute_url(self):
        return reverse("informe_detail", kwargs={"pk": self.pk}) 
    
    
class Logs(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Log de {self.usuario.username} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def get_absolute_url(self):
        return reverse("log_detail", kwargs={"pk": self.pk})