from django.db import models

# Create your models here.

class   GithubUser(models.Model):
    user_id = models.CharField(max_length=50, unique=True, blank=False, null=False)
    username = models.CharField(max_length=50, blank=False, null=False)
