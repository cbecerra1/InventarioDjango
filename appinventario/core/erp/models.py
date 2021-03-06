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

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f') #Para que me que con dos decimales
        return item

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
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.names
    
    def toJSON(self):
        item = model_to_dict(self)
        #item['gender'] = self.get_gender_display() #REtono el valor del display del mi choice
        item['gender'] = {'id':self.gender, 'name':self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d') #Conbierto a un formato el valor de la fecha
        return item

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

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]#PAra tener todo el detalle de la factura
        return item

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
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['sale']) #Excluimos sale porque es una relacion
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item