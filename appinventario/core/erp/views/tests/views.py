from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.forms import TestForm, TestForm2
from core.erp.models import Product, Category

#Para selects anidados
#Metodo 1
class TestView(TemplateView):
    #Puedo usar un formview, pero como no se  va a enviar inforamcions ni nada, uso mas vien un template view
    template_name = 'tests.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product_id':
                data = []
                for i in Product.objects.filter(cat_id=request.POST['id']):
                    data.append({'id': i.id, 'name': i.name})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    #Sobre escribo el metodo context_data para enviar valores adicionales a mi lista
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Select Aninados | Django'
        context['form'] = TestForm()
        return context

#Metodo 2
class TestView2(TemplateView):
    #Puedo usar un formview, pero como no se  va a enviar inforamcions ni nada, uso mas vien un template view
    template_name = 'tests2.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product_id':
                data = [{'id': '', 'text':'----------------------'}] #Como la data no tiene un  valor vacio ahi que inicializarla al comienzo
                for i in Product.objects.filter(cat_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.name, 'data':i.cat.toJSON()}) #PAra teruel eliminar la llave data porque no se necesitaria es ma un ejemplo
            #PAra el autocomplete
            elif action == 'autocomplete':
                data = []
                #Hago una busqueda de las categorias por el nombre lo que contiene la varialbe
                #No es recomendable que made toda la date, por eso pongo de 0 a 10 registros
                for i in Category.objects.filter(name__icontains=request.POST['term'])[0:10]:
                    item = i.toJSON()
                    #item['value'] = i.name #Le agrego otro dato al diccionario llamado value que contenga el nombre de la categoria
                    item['text'] = i.name #Este lo uso para poder trabajar con select2
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    #Sobre escribo el metodo context_data para enviar valores adicionales a mi lista
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Select Aninados | Django'
        context['form'] = TestForm2()
        return context