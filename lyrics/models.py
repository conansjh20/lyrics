from django.db import models

# Create your models here.
class Post(models.Model):
    song_model = models.CharField(max_length=30)
    singer_model = models.CharField(max_length=30)
    created_time = models.DateTimeField(auto_now_add=True)

