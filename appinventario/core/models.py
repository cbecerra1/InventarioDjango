from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_creation', 
                                        null=True, blank=True) #Para evitar problemas con las relaciones, digo comose va a llamar esa relacion
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_update', 
                                        null=True, blank=True)
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True #Con esto el modelo no se crea en mi tabla sino que lo creo para implementarlo en otras entidades
