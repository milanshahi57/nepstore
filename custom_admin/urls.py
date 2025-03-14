from django.urls import path
from .views import dashboard

urlpatterns = [
    path('', dashboard, name='custom_admin_dashboard'),
]
