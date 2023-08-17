# video_streaming_app/models.py

from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_path = models.URLField()

    def __str__(self):
        return self.title
