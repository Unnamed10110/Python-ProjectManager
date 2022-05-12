'''
formulario del modulo tipoUS
    - se validan los campos del formulario utilizado en la creacion de tipo de user story
'''
from django import  forms
from tipoUS.models import tipo_us
class tipo_usForm(forms.Form):
    '''clase de tipo de user story '''
    nombre = forms.CharField(max_length=100)
    descripcion= forms.CharField(max_length=100)

    def clean_nommbre(self):
        '''comprueba que no exista ningun tipo_us con el
        mismo nombre'''
        nombre = self.cleaned_data['nombre']
        if tipo_us.objects.filter(nombre=nombre):
           raise forms.ValidationError('EL TIPO DE HISTORIA DE USUARIO YA EXISTE')
        return nombre
