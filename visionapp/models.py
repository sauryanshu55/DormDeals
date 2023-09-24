from django.db import models

# Create your models here.
class ImageDescription(models.Model):
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True)