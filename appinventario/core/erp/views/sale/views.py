import json
from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.erp.forms import SaleForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Product, Sale, DetSale
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View

#Librerias para crear pdf
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class SaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'erp.view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod': #Para ver los detalles usando el id
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']): #El id del sale de la venta debe de ser igual al que me lelgo como parametro
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:sale_create')
        context['list_url'] = reverse_lazy('erp:sale_list')
        context['entity'] = 'Ventas'
        return context

class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model =  Sale
    form_class = SaleForm
    template_name = 'sale/create.html' 
    success_url = reverse_lazy('erp:sale_list')
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
                    #item['value'] = i.name #El autocomplete recive una variable llamada value que se necestia en la busqueda a media que se teclea
                    item['text'] = i.name #Porque asi recibe la data select2
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
                    data = {'id': sale.id} #Para tener la clave primaria de la factura que se genere

            else:
                data['error'] = 'No ha ingresado a ninguna opci??n'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #DEbo poner el  safe=False para serializarlo cuando es coleccion de elementos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creaci??n de una venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add' #Defino la accion que voy a hacer en el post, para hacerlo mas dinamico
        context['det'] = [] #CReo esta vairable porque la cree en editar pero se envia vacia
        return context

class SaleUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model =  Sale
    form_class = SaleForm
    template_name = 'sale/create.html' 
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'erp.change_sale'
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
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10] 
                for i in prods:
                    item = i.toJSON() 
                    #item['value'] = i.name 
                    item['text'] = i.name #Porque asi recibe la data select2
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic(): 
                    vents = json.loads(request.POST['vents']) 
                    #sale = Sale.objects.get(pk=self.get_object().id) #MAnera 1
                    sale = self.get_object() #MAnera 2, self.get_object() me devuelde la instancia del objeto que estoy editando
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    sale.detsale_set.all().delete() #Eliminamos la data anterior para evitar duplicidad

                    for i in vents['products']:
                        det = DetSale() 
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': sale.id} #Para tener la clave primaria de la factura que se genere
            else:
                data['error'] = 'No ha ingresado a ninguna opci??n'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) 

    #Metodo para traer los detalles de mi factura
    def get_details_product(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id): #Me da una instancia de la factura y accedemos a sus propiedades y los itero
            #DetSale.objects.filter(sale_id=self.kwargs['pk']) #Otra manera
                #Para que no se da??e mi estructura
                item = i.prod.toJSON() #TRaemos el producto, ahora lo podemos desmenuzar
                item['cant'] = i.cant #Le aumento la cantidad porque es el unico valor que necesito, los otros ya estan o me los calcula
                #EL subtotal no se envia porque se hace automaticamente con los procesos
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edici??n de una venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit' 
        context['det'] = json.dumps(self.get_details_product()) #Enviamos el metodo dentro de mi contexto
        return context

class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'erp.delete_sale'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminaci??n de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context

#Vista para crear mi archivo pdf
class SaleInvoicePdfView(View):

    #Creo el metodo para manejar archivos estaticos, agrego la palabra reservada self para que funcione
    #SE VE EN EL CAP 69, borre la carpeta staticfiles para que no se me haga pesado
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        #modifico la funcion segun la teoria del curso
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)
            
            # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path    

    #sobre escribimossu metodo get
    def get(self, request, *args, **kwars):
        try:
            # find the template and render it.
            template = get_template('sale/invoice.html') #Me devuelve un objeto de tipo template y debo decirle cual sera el objeto tipo html
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']), #La variable que corresponde con el objeto, kwards pk es el parametro que me va a llegar de la url
                'comp': {'name':'ALGORISOFT S.A', 'ruc': '98754123', 'address': 'Pereira, Colombia'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context) #Me permite incrustar parametros al objeto, aqui uso el diccionario
            #Creamos el objeto que va a devolver mi vista
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"' #Desactivo esta parte para que n se me descargue sino que vea el archivo en mi navegador
            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response, link_callback=self.link_callback)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:sale_list')) #Si ahi erro no imprime nada y me retorna al listado