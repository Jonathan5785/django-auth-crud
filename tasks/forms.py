from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate




# formulario para el registro de un usuario
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password','label':'Username'}))
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm your password'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username']
        labels = {
            'username':'Username'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter a username'}),
        }

# formulario para el inicio de sesion de un usuario
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request,username=username,password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    "Credenciales Incorrectas. Intentelo de nuevo.",
                    code = 'invalid_login',
                    params = {'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
            return self.cleaned_data




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Write a title'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
