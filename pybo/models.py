from django.db import models

# Create your models here.
# class Model을 상속.
from common.models import GithubUser

class   Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(GithubUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

class   Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(GithubUser, on_delete=models.CASCADE, null=True)
