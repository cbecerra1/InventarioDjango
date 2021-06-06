from django.forms import ModelForm
from .models import Category

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'#Las columnas del formulario, con [''] coloco el ordon y puedo hacer una exclusion de que cmapos no pongo en mi formulario
        