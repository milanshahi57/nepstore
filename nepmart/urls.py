from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.urls import path
from .views import product_list, product_detail,update_cart


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', update_cart, name='update_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
