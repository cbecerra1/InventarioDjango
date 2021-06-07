from django.forms import *
from .models import Category

class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Se hace un recorrido de los componentes del formulario (Esta en la variable self), haga una interacion de los cmapos que sean visibles
        #for form in self.visible_fields():
        #    form.field.widget.attrs['class'] = 'form-control'
        #    form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True #PAra que al momento de renderizar a este componente se le ponga el foco

    class Meta:
        model = Category
        fields = '__all__'#Las columnas del formulario, con [''] coloco el ordon y puedo hacer una exclusion de que cmapos no pongo en mi formulario
        #La parte de los labels la puedo omitir si use verbose name al crear el campo

        #Para personalizar mis componentes
        widgets = {
            'name' : TextInput(
                attrs ={
                    #'class':'form-control', #Ya lo hice arriba
                    'placeholder':'Ingrese un nombre',
                    #'autocomplete':'off'
                }
            ),
            'desc' : Textarea(
                attrs ={
                    #'class':'form-control',
                    'placeholder':'Ingrese una descripcón',
                    #'autocomplete':'off',
                    'rows':'3',
                    'cols':'3'
                }
            )
        }