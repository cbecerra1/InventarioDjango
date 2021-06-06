from django.http.response import JsonResponse
from django.shortcuts import render, redirect #Redirect me direcciona a la pagina dependido de la url que le mande
from django.urls import reverse_lazy #con reverse_lazy tengo la ruta absoluta de esa url
from django.utils.decorators import method_decorator
#from django.utils.decorators import method_decorator
#from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from erp.models import Category, Product
from django.views.generic import ListView, CreateView

from erp.models import Category, Product
from erp.forms import *

def category_list(request):
    data = {
        'title' : 'Listado de Categorias',
        'categories' : Category.objects.all()
    }
    return render(request, 'category/list.html', data)

class CategoryListView(ListView):

    model = Category
    template_name = 'category/list.html'

    #metodo dispatch, me redirecciona al metodo GET
    #Usamos un decorador para saber si un usario esta logeado, sino lo eta que se redireccione
    #@method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *arg, **kwargs):
        return super().dispatch(request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        #Cuando alguien haga una peticion de tipo post, me devuelva un objeto
        data = {}
        try:
            data = Category.objects.get(id=request.POST['id']).toJSON()   
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    #Podemos usar otros metodos, video 20, 
    #para obtener la consulta que queremos retornar a nuestra plantilla
    def get_queryset(self):
        #return Product.objects.all() #B. TEngo el mismo resultado que en A.
        #Nos sirve mucho para hacer validaciones
        #return Category.objects.filter(name__startswith="L") #Mosttrar los que empiecen con la letra b
        return Category.objects.all()
        
    #Como se la va a agregar mas datos a esta vista, se va a modificar ahi que sobreescrivirlo con el siguiente metodo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #Es un diccionario para poder agregarle mas variables
        #Puedo agregarle variables para devolver a mi plantilla
        context['title'] = 'Listado de Categorías'
        #context['object_list'] = Product.objects.all #A.Vemos el producto relacionado con las categorias, Tgo el mismo resultado que en A
        #print(reverse_lazy('erp:category_list')) #Para ver la funcion reverse_lazy
        return context

class CategoryCreateView(CreateView):
    model =  Category
    form_class = CategoryForm #Se le debe decir el formulario a trabajar
    template_name = 'category/create.html' #Se le dice el template o donde va a estar
    success_url = reverse_lazy('erp:category_list')#Donde redirecciono la plantilla luego de guardar, 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una categoria'
        return context