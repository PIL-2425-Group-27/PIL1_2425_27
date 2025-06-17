# reviews/urls.py

from django.urls import path
from .views import ReviewCreateView, ReviewListView, GlobalUserStatsView

urlpatterns = [
    path('', ReviewCreateView.as_view(), name='create-review'),
    path('<int:user_id>/', ReviewListView.as_view(), name='user-reviews'),
    path("stats/", GlobalUserStatsView.as_view(), name="global-user-stats"),
]
