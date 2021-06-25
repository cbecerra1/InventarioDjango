from django.db import models
from django.contrib.auth.models import AbstractUser

from config.settings import MEDIA_URL, STATIC_URL

# Create your models here.
#Creo una clase para reemplazar ami usuario
class User(AbstractUser):
    #Aumento los cmapos que me hacen falta, en este caso una imagen
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)#Se guarda por año por mes y por dia

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image) 
        return '{}{}'.format(STATIC_URL, 'img/empty.png')