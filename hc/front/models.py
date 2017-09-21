from django.db import models

class Blogs(models.Model):
    blog_post = models.CharField(max_length=20000, blank=False)
    user = models.TextField()
    title = models.CharField(max_length=200, blank=False)

# Create your models here.
