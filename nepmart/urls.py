from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.urls import path
from .views import product_list, product_detail


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', product_list, name='product_list'),
    path('products/<slug:slug>/', product_detail, name='product_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
