from apps.usuarios.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import Group
from django import forms

# Clase Formulario Crear Nuevo Usuaro
class CustomUserCreationForm(UserCreationForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(), 
        label='Rol', 
        required=True, 
        widget=forms.Select(
            attrs={'class': 'js-rol-single w-100'}
        ), 
        empty_label="Seleccione un rol"
    )
    IS_ACTIVE_CHOICES = ((True, 'Activo'), (False, 'Inactivo'),)
    is_active = forms.ChoiceField(
        label='Estado', 
        choices=IS_ACTIVE_CHOICES, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        # Personalización de los widgets
        self.fields['username'].widget.attrs.update({'placeholder': 'Ingresa el nombre de usuario'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ingresa los nombres'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ingresa los apellidos'})
        self.fields['password1'].widget.attrs.update({'maxlength': '12', 'placeholder': 'Ingresa la contraseña'})
        self.fields['password2'].widget.attrs.update({'maxlength': '12', 'placeholder': 'Confirma la contraseña'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Ingresa el correo electrónico'})
        self.fields['telefono'].widget.attrs.update({'placeholder': 'Ingresa el telefono'})
        self.fields['celular'].widget.attrs.update({'placeholder': 'Ingresa el celular'})
        self.fields['direccion'].widget.attrs.update({'placeholder': 'Ingresa la dirección'})

    # Validación de los campos
    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        if not groups:
            raise forms.ValidationError('Selecciona al menos un rol.')
        return groups

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'telefono', 'celular', 'direccion', 'groups', 'is_active']


# Clase Formulario Editar un Usuario 
class CustomUserEditionForm(forms.ModelForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(), 
        label='Rol', 
        required=True, 
        widget=forms.Select(
            attrs={'class': 'js-rol-single w-100'}
        ), 
        empty_label="Seleccione un rol"
    )
    IS_ACTIVE_CHOICES = ((True, 'Activo'), (False, 'Inactivo'),)
    is_active = forms.ChoiceField(
        label='Estado', 
        choices=IS_ACTIVE_CHOICES, 
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserEditionForm, self).__init__(*args, **kwargs)

        # Inicializar rol del usuario
        if self.instance and self.instance.pk:
            user_group = self.instance.groups.first()
            if user_group:
                self.initial['groups'] = user_group.id 

        # Personalización de los widgets
        self.fields['username'].widget.attrs.update({'placeholder': 'Ingresa el nombre de usuario'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ingresa los nombres'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ingresa los apellidos'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Ingresa el correo electrónico'})
        self.fields['telefono'].widget.attrs.update({'placeholder': 'Ingresa el telefono'})
        self.fields['celular'].widget.attrs.update({'placeholder': 'Ingresa el celular'})
        self.fields['direccion'].widget.attrs.update({'placeholder': 'Ingresa la dirección'})

    # Validación de los campos
    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        if not groups:
            raise forms.ValidationError('Selecciona al menos un rol.')
        return groups
    
    def clean_username(self):
        # Evita la validación única del username si no se ha modificado
        username = self.cleaned_data.get('username')
        if username == self.instance.username:
            return username
        
        # Si se modifica el username, realiza la validación estándar
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor, elige otro.")
        return username
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'celular', 'direccion', 'groups', 'is_active']


# Clase Formulario Editar Contraseña de Usuario
class CustomUserEditionPasswordForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserEditionPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'maxlength': '12', 'placeholder': 'Ingresa la contraseña'})
        self.fields['password2'].widget.attrs.update({'maxlength': '12', 'placeholder': 'Confirma la contraseña'})

    class Meta:
        model = CustomUser
        fields = ['password1', 'password2']


# Clase Formulario Editar Contraseña Perfil Usuario 
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'maxlength': '12', 'placeholder': 'Ingresa la contraseña antigua'})
        self.fields['new_password1'].widget.attrs.update({'maxlength': '12', 'placeholder': 'Ingresa la contraseña nueva'})
        self.fields['new_password2'].widget.attrs.update({'maxlength': '12', 'placeholder': 'Confirma la contraseña nueva'})


# Clase Formulario Editar Perfil Usuario 
class CustomUserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Ingresa el nombre de usuario'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ingresa los nombres'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ingresa los apellidos'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Ingresa el correo electrónico'})
        self.fields['telefono'].widget.attrs.update({'placeholder': 'Ingresa el telefono'})
        self.fields['celular'].widget.attrs.update({'placeholder': 'Ingresa el celular'})
        self.fields['direccion'].widget.attrs.update({'placeholder': 'Ingresa la dirección'})

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'telefono', 'celular', 'direccion')
