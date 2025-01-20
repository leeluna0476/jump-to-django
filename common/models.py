from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class   GithubUser(AbstractUser):
    access_token = models.CharField(max_length=255, blank=False, null=True)
    refresh_token = models.CharField(max_length=255, blank=False, null=True)
    password = None

    def __str__(self):
        return self.username
