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
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email')  # Display these fields
    search_fields = ('username', 'email')  # Search by username or email

admin.site.register(UserProfile, UserProfileAdmin)


