from django import forms
from django.utils import timezone

from .models import Animal, Raza


class AnimalForm(forms.ModelForm):
    especie = forms.ChoiceField(
        choices=(('perro', 'Perro'), ('gato', 'Gato')),
        label='Especie',
    )
    sexo = forms.ChoiceField(
        choices=(
            ('hembra', 'Hembra'),
            ('macho', 'Macho'),
            ('desconocido', 'Desconocido'),
        ),
        label='Sexo',
    )
    edad_aprox = forms.IntegerField(min_value=0, label='Edad aproximada (años)')
    peso = forms.IntegerField(min_value=0, label='Peso (kg)')
    foto_url = forms.URLField(required=False, label='URL de la foto')
    fecha_ingreso = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de ingreso',
    )

    class Meta:
        model = Animal
        fields = [
            'nombre',
            'raza',
            'especie',
            'edad_aprox',
            'sexo',
            'peso',
            'descripcion',
            'lugar_rescate',
            'condicion',
            'microchip',
            'foto_url',
            'fecha_ingreso',
        ]
        labels = {
            'nombre': 'Nombre (opcional)',
            'raza': 'Raza',
            'descripcion': 'Descripción',
            'lugar_rescate': 'Lugar de rescate',
            'condicion': 'Condición de salud',
            'microchip': 'Tiene microchip',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'microchip': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['raza'].queryset = Raza.objects.order_by('nomb_raza')
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'