from datetime import datetime
from django.forms import *
from core.erp.models import Category, Product, Client

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
                    'placeholder': 'Ingrese un nombre',
                    #'autocomplete':'off'
                }
            ),
            'desc' : Textarea(
                attrs ={
                    #'class':'form-control',
                    'placeholder': 'Ingrese una descripcón',
                    #'autocomplete':'off',
                    'rows': 3,
                    'cols': 3
                }
            )
        }

        #Para que no me aparezcan los campos en la creacion de la categoria
        #exclude = ['user_update', 'user_creation']
    
    #Metodo para guardar los datos
    def save(self, commit= True):
        data = {} #Creamos una variable para saber si tiene errores o no
        form = super() #REcuperamos el formulario
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    #Para hacer validaciones adicionales personalizadas
    #def clean(self):
        #PAra ver los objetos del formulario
    #    cleaned = super().clean()
        #Aplicamos una validacion
    #    if len(cleaned['name']) <= 50:
            #Hay dos maneras
    #        raise forms.ValidationError('Validacion xxx') #En esta solo me sale el error pero no me lo presenta, toca ponerle en el formularo una linea d e mas, ver documentacion django en form/api
            #self.add_error('name','Le faltan caracteres') #Hago una validacion adicional
    #    return cleaned

class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'cat': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
             data['error'] = str(e)
        return data

class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dni',
                }
            ),
            'date_birthday': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': Select()
        }
        #exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned

class TestForm(Form):
    #Creo un formulario que no se basa en un modelo
    #Puedo personalizar el componente y ponerle atirubtos
    #Queryset tiene el listado de objetos que se va a presentar
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))

    #Se pone none porque product debe de star vacio
    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control'
    }))

class TestForm2(Form):
    #Creo un formulario que no se basa en un modelo
    #Puedo personalizar el componente y ponerle atirubtos
    #Queryset tiene el listado de objetos que se va a presentar
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width:100%'
    }))

    #Se pone none porque product debe de star vacio
    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width:100%'
    }))

    #Para el autocompletado
    #search = CharField(widget=TextInput(attrs={
    #    'class': 'form-control',
    #    'placeholder': 'Ingrese una descripción'
    #}))

    #Para el autocompletado con select2
    search = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width:100%'
    }))
