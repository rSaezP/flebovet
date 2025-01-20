from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid': 'Por favor, ingresa un correo electrónico válido.',
            'required': 'El correo electrónico es obligatorio.'
        }
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        error_messages = {
            'username': {
                'required': 'El nombre de usuario es obligatorio.',
                'invalid': 'Ingresa un nombre de usuario válido. Solo puede contener letras, números y @/./+/-/_'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensajes de error de contraseña
        self.fields['password1'].error_messages = {
            'required': 'La contraseña es obligatoria.',
            'password_too_short': 'La contraseña debe tener al menos 8 caracteres.',
            'password_too_similar': 'La contraseña es muy similar a tu nombre de usuario.',
            'password_too_common': 'La contraseña es demasiado común.'
        }
        self.fields['password2'].error_messages = {
            'required': 'Por favor, confirma tu contraseña.',
            'password_mismatch': 'Las contraseñas no coinciden.'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email