from django.db import models

# Create your models here.

#home page adds


class Advertisement(models.Model):
    title = models.CharField(max_length=255, blank=True)  # Making the title optional
    image = models.ImageField(upload_to='ads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Advertisement {self.id}" if not self.title else self.title


