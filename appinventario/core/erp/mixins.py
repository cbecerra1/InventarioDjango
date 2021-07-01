from typing import Sequence
from django.shortcuts import redirect
from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

#Va a validar si un usario es super user
class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        #Si un usuario esta logeado le damos acceso a nuestra vista
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')
    
    #Para enviar valores adicionales
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #Es un diccionario para poder agregarle mas variables
        context['date_now'] = datetime.now()
        return context

#Mixin para permisos
class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    #Le modifico la url a retornar
    url_redirect = None

    #Creo metodo para los permisos
    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms        

    #Validamos la url
    def get_url_redirect(self):
        #Si esta vacio ne lo envie al login
        if self.url_redirect is None:
            return reverse_lazy('login')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        #Si un usuario esta logeado le damos acceso a nuestra vista
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para ingresar a este modulo')
        return HttpResponseRedirect(self.get_url_redirect())