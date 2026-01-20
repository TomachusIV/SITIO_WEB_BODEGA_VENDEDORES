from django import forms
from django.contrib.auth.forms import AuthenticationForm

from SISTEMA.models.models import Cliente, Usuario, PosibleCliente, InformeVendedor

from SISTEMA.utils.utils import procesar_datos_informe, validar_rut

class InformeVendedorForm(forms.ModelForm):
    fecha_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        label='Hora Inicio Gestión'
    )
    fecha_termino = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        label='Hora Término Gestión'
    )

    class Meta:
        model = InformeVendedor
        fields = [
            'cliente', 
            'fecha_inicio', 
            'fecha_termino', 
            'metodo_contacto', 
            'metodo_pago', 
            'tipo_producto', 
            'venta_realizada', 
            'descripcion'
        ]
        
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            
            'tipo_producto': forms.CheckboxSelectMultiple(attrs={
                'class': 'checkbox-container'
            }),
            
            'metodo_contacto': forms.Select(attrs={'class': 'form-select'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'venta_realizada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Detalles u observaciones...'
            }),
        }
        
        labels = {
            'cliente': 'Cliente Visitado',
            'venta_realizada': '¿Se concretó venta?',
            'tipo_producto': 'Productos de interés',
            'metodo_contacto': 'Vía de contacto',
            'metodo_pago': 'Forma de pago',
            'descripcion': 'Observaciones',
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            cleaned_data = procesar_datos_informe(cleaned_data)
        return cleaned_data


class PosibleClienteForm(forms.ModelForm):
    rut = forms.CharField(
        label='RUT',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control rut-input',
            'placeholder': 'Ej: 11.222.333-4',
            'maxlength': '12'
        }),
        validators=[validar_rut]
    )

    class Meta:
        model = PosibleCliente
        fields = [
            'rut', 
            'nombre_comercio',
            'nombre', 
            'apellido', 
            'email', 
            'telefono', 
            'ubicacion',
            'descripcion'
        ]
        
        widgets = {
            'nombre_comercio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del negocio (Opcional)'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+569...'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección / Ciudad'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
        labels = {
            'nombre_comercio': 'Nombre Comercio / Fantasía',
            'nombre': 'Nombre Contacto',
            'apellido': 'Apellido Contacto',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'ubicacion': 'Dirección',
            'descripcion': 'Notas / Intereses',
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            return rut.upper().replace('.', '').replace('-', '')
        return rut


class ClienteForm(forms.ModelForm):
    rut = forms.CharField(
        label='RUT Cliente',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control rut-input',
            'placeholder': 'Ej: 11.111.111-1',
            'maxlength': '12'
        }),
        validators=[validar_rut]
    )

    class Meta:
        model = Cliente
        fields = [
            'rut', 
            'nombre_comercio', 
            'nombre', 
            'apellido', 
            'email', 
            'telefono', 
            'ubicacion', 
            'tipo_cliente'
        ]
        
        widgets = {
            'nombre_comercio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del negocio (si aplica)'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+569...'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'tipo_cliente': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'nombre_comercio': 'Nombre Fantasía / Comercio',
            'nombre': 'Nombre Contacto',
            'apellido': 'Apellido Contacto',
            'tipo_cliente': 'Tipo de Cliente (Asignar ahora)',
            'ubicacion': 'Dirección Comercial'
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            return rut.upper().replace('.', '').replace('-', '')
        return rut


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Nombre de usuario',
        'style': 'width: 100%;'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Contraseña',
        'style': 'width: 100%;'
    }))
    
    class Meta:
        model = Usuario
        fields = ['username', 'password']


class ReporteExportForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Desde'
    )
    fecha_termino = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Hasta'
    )