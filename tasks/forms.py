from django import forms
from .models import Task,User


from django.contrib.auth import authenticate


from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
)
from django.forms.models import modelform_factory


CustomUserCreationForm = modelform_factory(
    User,
    fields=(
        'username',
        'password',
        'first_name',
        'last_name',
        'role',
        'is_active',
    ),
    labels={
        'username':'Usuario',
        'password':'Contraseña',
        'first_name':'Nombres',
        'last_name':'Apellidos',
        'role':'Rol',
        'is_active':'Activo',
    },
)



UserUpdateForm = modelform_factory(
    User,
    fields=(
        'username',
        'first_name',
        'last_name',
        'role',
        'is_active',
    ),
    labels={
        'username':'Usuario',
        'first_name':'Nombres',
        'last_name':'Apellidos',
        'role':'Rol',
        'is_active':'Activo',
    },
)




# # formulario para el registro de un usuario
# class CustomUserCreationForm(UserCreationForm):
#     password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password','label':'Username'}))
#     password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm your password'}))
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ['username']
#         labels = {
#             'username':'Username'
#         }
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter a username'}),
#         }


from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
)
from django.core.exceptions import ValidationError

class AuthenticationForm(BaseAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        # Personalizar el mensaje de error por credenciales incorrectas
        self.error_messages['invalid_login'] = 'Credenciales incorrectas. Inténtelo de nuevo.'
        # Personalizar el mensaje de error por usuario inactivo
        # self.error_messages['inactive'] = 'Esta cuenta está inactiva. Contacte al administrador.'
    
    # def confirm_login_allowed(self, user: AbstractBaseUser) -> None:
    #     print(f"User is_active: {user.is_active}")  # Comprobar si el método se está ejecutando
    #     if not user.is_active:
    #         raise forms.ValidationError('Esta cuenta no está activa.',code="inactive")
        
    #     return super().confirm_login_allowed(user)
# # formulario para el inicio de sesion de un usuario
# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
#     password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')

#         if username and password:
#             self.user_cache = authenticate(self.request,username=username,password=password)

#             if self.user_cache is None:
#                 raise forms.ValidationError(
#                     "Credenciales Incorrectas. Intentelo de nuevo.",
#                     code = 'invalid_login',
#                     params = {'username': self.username_field.verbose_name},
#                 )
#             else:
#                 self.confirm_login_allowed(self.user_cache)
#             return self.cleaned_data




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']
        # Les quite el 'class':'form-control' porque ya lo estoy cubriendo con la funcionalidad de crispy
        # Ahora el atributo widgtes lo uso solamente para poner placeholder
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Write a title'}),
            'description': forms.Textarea(attrs={'placeholder':'Write a description'}),
            # 'important': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
