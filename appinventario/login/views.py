from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView, RedirectView
from django.urls import reverse_lazy

# Create your views here.
#Puedo usar cualqueira de las dos opciones para iniciar login
class LoginFormView(LoginView):
    template_name  = 'login.html'

    #PAra ver si tengo mi inicio de sesion dentro de mi sistema, si el usuario esta logeado
    def dispatch(self, request, *args, **kwargs):
        #Hago una validacion
        if request.user.is_authenticated:
            return redirect('erp:category_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesion'
        return context

class LoginFormView2(FormView):
    #El formview trabaj con un formulario
    form_class = AuthenticationForm
    template_name  = 'login.html'
    success_url = reverse_lazy('erp:category_list')

    #PAra ver si tengo mi inicio de sesion dentro de mi sistema, si el usuario esta logeado
    def dispatch(self, request, *args, **kwargs):
        #Hago una validacion
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user()) #Optenemos el usuario
        #Hacemos inicio de sesion
        return HttpResponseRedirect(self.success_url) #Vamos a nuestra vista de exito

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesion'
        return context

class LogoutRedirectView(RedirectView):
    pattern_name='login'

    def dispatch(self, request, *args, **kwargs):
        #Para cerrar sesion
        logout(request)
        return super().dispatch(request, *args, **kwargs)    
