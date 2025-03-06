from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)  # ✅ Add this
    image = models.ImageField(upload_to='products/')
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Add this

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



# contact form submission 

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#user registration

class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password

    def __str__(self):
        return self.username  # Display username in Django admin
