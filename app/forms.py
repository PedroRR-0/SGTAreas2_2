from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from app.models import Usuario, Tarea


class LoginForm(forms.Form):
    user = forms.CharField(max_length=50, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


class RegistroForm(forms.Form):
    user = forms.CharField(max_length=50, label="Usuario",
                           widget=forms.TextInput(
                               attrs={'pattern': '^[a-zA-Z0-9]{3,}$',
                                      'title': 'Solo se permiten letras y números, mínimo 3 caracteres.'}
                           ))
    nombre = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'pattern': '[a-zA-Z ]+', 'title': 'Solo se permiten letras y espacios.'}))
    apellidos = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'pattern': '[a-zA-Z ]+', 'title': 'Solo se permiten letras y espacios.'}))
    tlf = forms.CharField(max_length=12,
                          widget=forms.TextInput(attrs={'pattern': '[0-9]+', 'title': 'Solo se permiten números.'}))
    mail = forms.CharField(max_length=50, widget=forms.EmailInput(
        attrs={'pattern': '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}',
               'title': 'Introduce una dirección de correo electrónico válida.'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'pattern': '^(?=.*\\d)(?=.*[a-zA-Z]).{8,}$',
                                                                 'title': 'Debe contener al menos 8 caracteres, una '
                                                                          'letra y un número.'}),
                               label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirma contraseña")

    def clean_user(self):
        username = self.cleaned_data['user']
        if Usuario.objects.filter(user=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor, elige otro.")
        return username


class NuevaTareaForm(forms.ModelForm):
    usuarios = forms.ModelMultipleChoiceField(queryset=Usuario.objects.all(), widget=forms.CheckboxSelectMultiple)
    prioridad = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 10})
    )

    class Meta:
        model = Tarea
        fields = ['nombre', 'prioridad', 'fecha_vencimiento', 'usuarios']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(NuevaTareaForm, self).__init__(*args, **kwargs)
        self.fields['usuarios'].queryset = Usuario.objects.all()


class ModificarTareaForm(forms.ModelForm):
    usuarios = forms.ModelMultipleChoiceField(queryset=Usuario.objects.all(), widget=forms.CheckboxSelectMultiple)
    prioridad = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 10})
    )

    class Meta:
        model = Tarea
        fields = ['nombre', 'prioridad', 'fecha_vencimiento', 'usuarios']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ModificarTareaForm, self).__init__(*args, **kwargs)
        self.fields['usuarios'].queryset = Usuario.objects.all()
