from django.forms import *

#Creamos el componente para el filtro, campo charfield y componente tipo textinput,
#DEspues de tenerlo lo llamo en mi vista de los reportes
class ReportForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
