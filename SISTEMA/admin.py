from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, 
    Rol, 
    TipoProducto, 
    MetodoContacto, 
    MetodoPago, 
    TipoCliente
)

# 1. Configuración especial para el Usuario personalizado
@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Campos que se muestran en la lista (tabla)
    list_display = ('username', 'email', 'rut', 'rol', 'is_staff', 'is_active')
    
    # Campos por los que se puede buscar
    search_fields = ('username', 'email', 'rut', 'first_name', 'last_name')
    
    # Filtros laterales
    list_filter = ('rol', 'is_staff', 'is_active', 'groups')

    # Agregamos los campos personalizados (rut y rol) al formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información Extra', {'fields': ('rut', 'rol')}),
    )
    
    # Agregamos los campos al formulario de creación de usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Extra', {'fields': ('rut', 'rol')}),
    )

# 2. Configuración para Rol
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion') # Muestra ID para referencia fácil
    search_fields = ('nombre',)
    ordering = ['nombre']

# 3. Configuración para TipoProducto
@admin.register(TipoProducto)
class TipoProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

# 4. Configuración para MetodoContacto
@admin.register(MetodoContacto)
class MetodoContactoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

# 5. Configuración para MetodoPago
@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

# 6. Configuración para TipoCliente
@admin.register(TipoCliente)
class TipoClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)