from django.core.exceptions import ValidationError
from django.utils import timezone
from itertools import cycle

def procesar_datos_informe(cleaned_data):
    
    from SISTEMA.models.models import MetodoPago, TipoProducto
    
    venta_realizada = cleaned_data.get('venta_realizada')
    hora_inicio = cleaned_data.get('fecha_inicio')
    hora_termino = cleaned_data.get('fecha_termino')
    
    if hora_inicio and hora_termino:
        if hora_termino <= hora_inicio:
            raise ValidationError({'fecha_termino': 'La hora de término debe ser mayor a la de inicio.'})
        
        hoy = timezone.now().date()
        cleaned_data['fecha_inicio'] = timezone.datetime.combine(hoy, hora_inicio)
        cleaned_data['fecha_termino'] = timezone.datetime.combine(hoy, hora_termino)

    if not venta_realizada:
        try:
            metodo_pago_na = MetodoPago.objects.get(nombre="N/A")
            tipo_producto_na = TipoProducto.objects.get(nombre="N/A")
            
            cleaned_data['metodo_pago'] = metodo_pago_na
            cleaned_data['tipo_producto'] = [tipo_producto_na]
            
        except MetodoPago.DoesNotExist:
            raise ValidationError({'metodo_pago': 'Error crítico: No existe la opción "N/A" en base de datos.'})
        except TipoProducto.DoesNotExist:
            raise ValidationError({'tipo_producto': 'Error crítico: No existe la opción "N/A" en base de datos.'})

    return cleaned_data


def procesar_datos_informe(cleaned_data):
    """
    Lógica de negocio para validar fechas y gestionar casos de 'No Venta'.
    """
    from SISTEMA.models import MetodoPago, TipoProducto

    venta_realizada = cleaned_data.get('venta_realizada')
    hora_inicio = cleaned_data.get('fecha_inicio')
    hora_termino = cleaned_data.get('fecha_termino')
    
    if hora_inicio and hora_termino:
        if hora_termino <= hora_inicio:
            raise ValidationError({'fecha_termino': 'La hora de término debe ser mayor a la de inicio.'})
        
        hoy = timezone.now().date()
        cleaned_data['fecha_inicio'] = timezone.datetime.combine(hoy, hora_inicio)
        cleaned_data['fecha_termino'] = timezone.datetime.combine(hoy, hora_termino)

    if not venta_realizada:
        try:
            metodo_pago_na = MetodoPago.objects.get(nombre="N/A")
            tipo_producto_na = TipoProducto.objects.get(nombre="N/A")
            
            cleaned_data['metodo_pago'] = metodo_pago_na
            cleaned_data['tipo_producto'] = [tipo_producto_na]
            
        except MetodoPago.DoesNotExist:
            raise ValidationError({'metodo_pago': 'Error crítico: No existe la opción "N/A" en MetodoPago.'})
        except TipoProducto.DoesNotExist:
            raise ValidationError({'tipo_producto': 'Error crítico: No existe la opción "N/A" en TipoProducto.'})

    return cleaned_data

def validar_rut(rut):
    """
    Valida que un RUT chileno sea matemáticamente correcto Y tenga un largo válido.
    """
    if not rut: return 

    # 1. Limpieza (Quitamos puntos y guión)
    rut_limpio = rut.replace('.', '').replace('-', '').upper().strip()
    
    # --- NUEVA VALIDACIÓN DE TAMAÑO ---
    # Un RUT 'crudo' (sin puntos ni guión) debe tener:
    # Mínimo 8 caracteres: Ej: 1.000.000-1 -> "10000001"
    # Máximo 9 caracteres: Ej: 99.999.999-9 -> "999999999"
    if len(rut_limpio) < 8:
        raise ValidationError("El RUT es demasiado corto (Mínimo 1 millón).")
    
    if len(rut_limpio) > 9:
        raise ValidationError("El RUT excede el largo permitido.")
    # ----------------------------------

    cuerpo = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]

    if not cuerpo.isdigit():
        raise ValidationError("El cuerpo del RUT debe contener solo números.")

    # 2. Algoritmo Módulo 11
    try:
        rev_cuerpo = map(int, reversed(cuerpo))
        factors = cycle(range(2, 8))
        s = sum(d * f for d, f in zip(rev_cuerpo, factors))
        mod = (-s) % 11
        
        if mod == 10:
            dv_calculado = 'K'
        else:
            dv_calculado = str(mod)
            
    except Exception:
        raise ValidationError("Error al calcular el dígito verificador.")

    # 3. Comparación
    if dv_ingresado != dv_calculado:
        raise ValidationError(f"RUT inválido. (El dígito verificador no coincide).")