from crum import get_current_user
from django.db import models
from datetime import datetime

from django.forms import model_to_dict

from config.settings import STATIC_URL, MEDIA_URL
from core.erp.choices import gender_choices
from core.models import BaseModel

# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    #usando la libreria django-crum sobreescribo mi metodo de guardado
    def save(self, force_insert=False, force_update=False, using=None,
                update_fields=None):
        #Aqui digo que va a pasr cuando hago un guardado
        #Obtengo el usuario que tengo en el momento y lo guardo
        user = get_current_user()
        #Validamos que el usuario exista
        if user is not None:
            if not self.pk:
                self.user_creation = user #Si el usuario no existe lo crea
            else:
                self.user_update = user
        super(Category, self).save()

    #El sighiente metodo me devuelve un diccionario con todos los atributos que tiene mi entidad
    def toJSON(self):
        item = model_to_dict(self) #Self contiene la entidad en si, entonces me pasa todo a diccionario
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

#mirar el video 42 donde muestra sin el metodo ajax
class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoria')
    image = models.ImageField(upload_to='product/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.name

    #Metodo para que sea mas eficiente
    def get_image(self):
        if self.image: #En caso de que la imagen tenga datos
            return '{}{}'.format(MEDIA_URL, self.image) #Me retorna la ruta con la imagen
        return '{}{}'.format(STATIC_URL, 'img/empty.png') #Sino retorna una imagen por defecto

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    sexo = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.names

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']

class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']