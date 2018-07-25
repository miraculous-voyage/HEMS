# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Extrainfo(models.Model):
    user_name = models.CharField(max_length=255)
    user_image = models.ImageField(upload_to='images/', default='/images/default.png')

    def __str__(self):
        return str(self.user_name)