from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.urls import reverse_lazy #con reverse_lazy tengo la ruta absoluta de esa url
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from erp.models import Category, Product
from erp.forms import *

class CategoryListView(ListView):

    model = Category
    template_name = 'category/list.html'

    #metodo dispatch, me redirecciona al metodo GET
    #Usamos un decorador para saber si un usario esta logeado, sino lo eta que se redireccione
    #@method_decorator(login_required)
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *arg, **kwargs):
        #Cuando alguien haga una peticion de tipo post, me devuelva un objeto
        data = {}
        try:
            action = request.POST['action']
            #Cuando hacemos varias acciones en el post es bueno manejar un identificador
            if action == 'searchdata':
                data = []
                for i in Category.objects.all():
                    data.append(i.toJSON()) #retorno como resultado una collecion diccionario con todos los elementos de mi tabla
            else:
                data['error'] = 'Ha ocurrido un error'
            #data = Category.objects.get(id=request.POST['id']).toJSON()   
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

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
        context['create_url'] = reverse_lazy('erp:category_create') #PAra mandar la ruta absoluta
        #context['object_list'] = Product.objects.all #A.Vemos el producto relacionado con las categorias, Tgo el mismo resultado que en A
        #print(reverse_lazy('erp:category_list')) #Para ver la funcion reverse_lazy
        context['list_url'] = reverse_lazy('erp:category_list')
        context['entity'] = 'Categorias'
        return context

class CategoryCreateView(CreateView):
    model =  Category
    form_class = CategoryForm #Se le debe decir el formulario a trabajar
    template_name = 'category/create.html' #Se le dice el template o donde va a estar
    success_url = reverse_lazy('erp:category_list')#Donde redirecciono la plantilla luego de guardar, 

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    #Ejemplo, metodo post para los errores
    def post(self, request, *arg, **kwargs):
        data = {}
        try:
            #Recuperamos la variable action, me sale en el diccionario que me arroja ajax
            action = request.POST['action']#Cada vez que alguien haga una peticion me manda un action para saber que se va a a hacer
            if action == 'add':
                form = self.get_form() #Obtenemos el formulario ccon tdos los datos
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    #    print(request.POST)
    #    form = CategoryForm(request.POST) #Le ponemos al formulario lo que esta llegando del post
    #    
    #    if form.is_valid():
    #        form.save()
    #        return HttpResponseRedirect(self.success_url) #PAra redireccionar a una url
    #    
    #    self.object = None
    #    context = self.get_context_data(**kwargs) #Este pedazo aca es para poder meterlo dentro de la caja
    #    context['form'] = form
    #    return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'add' #Defino la accion que voy a hacer en el post, para hacerlo mas dinamico
        return context

class CategoryUpdateView(UpdateView):
    model =  Category
    form_class = CategoryForm 
    template_name = 'category/create.html'
    success_url = reverse_lazy('erp:category_list') 

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object() #Importante seguir este parametro para la edicion, ya que ahi que asignarle el objeto sino django lo toma que un objeto nuevo que va a creaer
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *arg, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form() 
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'edit' 
        return context

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/delete.html'
    success_url = reverse_lazy('erp:category_list') 

    #@method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:category_list')
        return context

class CategoryFormView(FormView):
    #Verifica que mi formulario sea valido
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('erp:category_list')

    #Sobreescribimos dos metodos que son propios y se usan mucho en esta vista generica
    def form_valid(self, form):#si se ejecuta de manera correcta
        print(form.is_valid())
        print(form)
        return super().form_valid(form)
    
    def form_invalid(self, form):#Para ver el error
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'form | Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'add' #Defino la accion que voy a hacer en el post, para hacerlo mas dinamico
        return context  