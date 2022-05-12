'''Formulario utilizado para guardar los datos y luego validarlos, de los usuario que intentan acceder
 al sistema'''
from django import forms
class loginform(forms.Form):
    """
        Guarda los campos Username y Password en el formulario
        :param recibe como argumento la clase formulario de Django
    """
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())
