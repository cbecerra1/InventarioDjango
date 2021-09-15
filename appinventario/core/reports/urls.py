
from core.reports.views import ReportSaleView
from django.urls.conf import path

urlpatterns = [
    # Reports
    path('sale/', ReportSaleView.as_view(), name='sale_report'),
]
