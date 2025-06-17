from django.urls import path
from .views import generate_meeting_point, confirm_meeting_point, get_eta_view

urlpatterns = [
    path("point/generate/", generate_meeting_point, name="generate-meeting-point"),
    path("point/confirm/", confirm_meeting_point, name="confirm-meeting-point"),
    path("eta/", get_eta_view, name="eta"),
]
