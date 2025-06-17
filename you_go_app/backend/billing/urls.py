from django.urls import path
from .views import (
    InvoiceListView, InvoiceDetailView,
    InvoicePDFDownloadView, GenerateInvoiceView
)

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice-list'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('download/', InvoicePDFDownloadView.as_view(), name='invoice-download'),
    path('generate/', GenerateInvoiceView.as_view(), name='invoice-generate'),
]
