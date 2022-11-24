from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()