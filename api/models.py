from django.db import models

# Create your models here.
class Image(models.Model):
    original_image = models.ImageField(upload_to='original_images/')
    anonymized_image = models.ImageField(upload_to='anonymized_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image {self.id}"
