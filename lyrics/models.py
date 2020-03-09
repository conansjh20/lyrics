from django.db import models

# Create your models here.
class Post(models.Model):
    singersong = models.CharField()
    created_time = models.DateTimeField(auto_now_add=True)

