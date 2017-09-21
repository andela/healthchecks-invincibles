from django.db import models
from django.utils import timezone
from embed_video.fields import EmbedVideoField


class Blogs(models.Model):
    blog_post = models.CharField(max_length=20000, blank=False)
    user = models.TextField()
    title = models.CharField(max_length=200, blank=False)

class Blogs(models.Model):
    blog_post = models.CharField(max_length=20000, blank=False)
    user = models.TextField()
    title = models.CharField(max_length=200, blank=False)

# Create your models here.

class Faq(models.Model):
    """This class handles Frequent Questions and Answers"""
    question = models.CharField(max_length=800)
    answer = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question

class Video(models.Model):
    """This class handles videos """
    title = models.CharField(max_length=800)
    video = EmbedVideoField()  # same like models.URLField()

    def __str__(self):
        return self.title
