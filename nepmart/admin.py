from django.contrib import admin
from .models import Product, ContactMessage  # Ensure Product model exists in models.py

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')  # Ensure 'created_at' exists in Product model
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # Ensure 'slug' exists in Product model

admin.site.register(Product, ProductAdmin)


# For contact page submission
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')

# customer registration 

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
