from django.db import models

class Page(models.Model):
    title = models.CharField(max_length = 16)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    version = models.IntegerField()
