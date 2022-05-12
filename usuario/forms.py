from django import forms
from django.contrib.auth.models import User


class RegistroUserForm(forms.Form):
    '''Utiliza la autentificacion de usuario que proporciona Django. '''
    username = forms.CharField(min_length=5)
    email = forms.EmailField()
    password = forms.CharField(min_length=5, widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    #photo = forms.ImageField(required=False)

    def cleanUsername(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def cleanEmail(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual en la db.')
        return email

    def cleanPassword2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contrasenhas no coinciden.')
        return password2



class cambiocontra(forms.Form):
    passanterior = forms.CharField(min_length=5, widget=forms.PasswordInput())
    password1 = forms.CharField(min_length=5, widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

class eliminarusuarios:
    username = forms.CharField(min_length=5)
    email = forms.EmailField()
