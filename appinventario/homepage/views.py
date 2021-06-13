from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    #Renderia una plantilla donde se mande el siguiene parametro
    template_name = 'index.html'

    #Puedo usar los metodos de la vista