from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    summary = models.CharField(max_length=256, null=False, blank=False)
    content = models.TextField(null=False, blank=False)