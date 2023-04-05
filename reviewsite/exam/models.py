from django.db import models
from django.utils import timezone

# Create your models here.

class Movie(models.Model):
    genre = models.CharField(max_length=20)
    movie_name = models.CharField(max_length=100)
    movie_summary = models.TextField()
    reg_date = models.DateTimeField(default=timezone.now)