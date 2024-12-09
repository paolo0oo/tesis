from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, TipoProducto


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class ProductoForm(forms.ModelForm):
    
    class Meta:
        model = Producto
        fields = '__all__'

class TipoProdForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['Tipo_prod'] 

class TipoProductoForm(forms.ModelForm):
    class Meta:
        model = TipoProducto
        fields = ['nombre']