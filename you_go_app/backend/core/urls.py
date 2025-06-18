from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),           # Authentication
    path('api/active-status/', include('accounts.urls')),  # Active status endpoint
    # add other app URLs here...
]
