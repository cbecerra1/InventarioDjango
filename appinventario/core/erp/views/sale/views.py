import json
from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.erp.forms import SaleForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Product, Sale, DetSale
from django.views.generic import CreateView, ListView, DeleteView

class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model =  Sale
    form_class = SaleForm
    template_name = 'sale/create.html' 
    success_url = reverse_lazy('index')
    permission_required = 'erp.add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *arg, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10] #Buscamos por el nombre, y recibo la variable que va a contener la busqueda, en este caso la variable term
                # Itero los productos
                for i in prods:
                    item = i.toJSON() #Uso el diccionario ya creado
                    #Devuelvo un array con un diccionario de los productos
                    item['value'] = i.name #El autocomplete recive una variable llamada value que se necestia en la busqueda a media que se teclea
                    #item['cant'] = 1 es la otra opcion quitando la de form.js, prefiero esta
                    data.append(item)
            elif action == 'add':
                with transaction.atomic(): #Por si ahi un error para que django no guarde lo que se estaba f uardadno
                    vents = json.loads(request.POST['vents']) #El post debe de ser convertido a json
                    sale = Sale() #Para la tabla de  venta
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()

                    #Iteramos los productos
                    for i in vents['products']:
                        det = DetSale() #PAra la tabla del  detalle de la venta
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #DEbo poner el  safe=False para serializarlo cuando es coleccion de elementos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add' #Defino la accion que voy a hacer en el post, para hacerlo mas dinamico
        return context
