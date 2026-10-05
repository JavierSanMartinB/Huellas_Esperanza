import bcrypt
from django import forms
from .models import Usuario

class UserForm(forms.ModelForm):
    correo = forms.EmailField(max_length=50, label='Correo electrónico')
    direccion = forms.CharField(max_length=50, label='Dirección')
    telefono = forms.IntegerField(min_value=0, max_value=999999999, label='Teléfono')
    contrasena = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Usuario
        fields = [
            'nomb', 'ap_paterno', 'ap_materno', 'correo',
            'fecha_nac', 'direccion', 'telefono', 'contrasena', 'password2'
        ]
        labels = {
            'nomb': 'Nombre',
            'ap_paterno': 'Apellido paterno',
            'ap_materno': 'Apellido materno',
            'correo': 'Correo electrónico',
            'fecha_nac': 'Fecha de nacimiento',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'contrasena': 'Contraseña',
        }

        widgets = {
            'contrasena': forms.PasswordInput,
            'fecha_nac': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('contrasena')
        password_confirmation = cleaned_data.get('password2')

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password2', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.contrasena_hash = bcrypt.hashpw(
            self.cleaned_data['contrasena'].encode('utf-8'),
            bcrypt.gensalt(),
        ).decode('utf-8')
        if commit:
            usuario.save()
        return usuario
