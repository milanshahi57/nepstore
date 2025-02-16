from django.shortcuts import render, redirect

# Create your views here.



#trend image display
from .models import Advertisement

def home(request):
    ads = Advertisement.objects.all()  # Get all advertisements
    return render(request, 'home.html', {'ads': ads})


