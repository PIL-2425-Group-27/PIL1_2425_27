from django.urls import path
from .views import RegisterView, ActiveStatusView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('active-status/', ActiveStatusView.as_view(), name='active-status'),
]
