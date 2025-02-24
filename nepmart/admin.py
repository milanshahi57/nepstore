from django.contrib import admin
from .models import Product  # Ensure Product model exists in models.py

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')  # Ensure 'created_at' exists in Product model
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # Ensure 'slug' exists in Product model

admin.site.register(Product, ProductAdmin)
