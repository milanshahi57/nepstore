from django.contrib import admin

# Register your models here.
#add in homepage
from .models import Advertisement

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'created_at')
    search_fields = ('title',)

admin.site.register(Advertisement, AdvertisementAdmin)
