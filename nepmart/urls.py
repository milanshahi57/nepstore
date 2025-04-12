from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.urls import path
from .views import register_user, login_view
from .views import product_list, product_detail,update_cart
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path("register/", register_user, name="register_user"), 
    path('login/', login_view, name='login'),
    path('products/', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', update_cart, name='update_cart'),
    path('contact/', views.contact_view, name='contact'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
