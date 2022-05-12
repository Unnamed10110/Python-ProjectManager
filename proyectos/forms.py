from django import  forms
from proyectos.models import Proyecto
class ProyectoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    scrum_master = forms.CharField(max_length=100)
    fechaInicio=forms.DateField()
    fechaFin = forms.DateField()

    def clean_nommbre(self):
        """comprueba que no exista ningun proyecto con el
        mismo nombre"""
        nombre = self.cleaned_data['nombre']
        if Proyecto.objects.filter(nombre=nombre):
           raise forms.ValidationError('NOMBRE DEL PROYECTO YA EXISTE')
        return nombre
    def clean_scrum_master(self):
        """comprueba que el scrum master exista"""
        scrum = self.cleaned_data['scrum']
        if Proyecto.objects.filter(nombre=scrum):
            raise forms.ValidationError('NOMBRE DEL PROYECTO YA EXISTE')
        return scrum
    def clean_fecha(self):
        fecha1 = self.cleaned_data['fechaInicio']
        fecha2 = self.cleaned_data['fechaFin']
        if fecha1 == fecha2:
            raise forms.ValidationError('Las Fechas deben ser distintas')
        if fecha1 > fecha2:
            raise forms.ValidationError('Fecha Inicio mayor al Fin')
