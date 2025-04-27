from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(label='Nombre', required=True, widget=forms.TextInput)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', required=True, widget=forms.PasswordInput)
    foto = forms.ImageField(required=False)

    class Meta:
        model = Perfil
        fields = ['username', 'email', 'password1', 'password2', 'foto']