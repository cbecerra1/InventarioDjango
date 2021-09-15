from core.reports.forms import ReportForm
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy #PAra poner la ruta absoluta de una url

# Create your views here.
#uso solo esta porque es un solo ejemplo, si fueran mas reportes lo haria en erp por separado cada reporte, cap 71
class ReportSaleView(TemplateView):
    template_name = 'sale/report.html'

    #Sobreescribimos el contex data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #Lo sobreescribimos para poner informacion adicional
        context['title'] = 'Reporte de las ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('sale_report')
        context['form'] = ReportForm() #importo mi componente creado en forms
        return context