import datetime

from django.contrib.auth.models import User
from django.db import models

class ToDo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    important = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    deadline_datetime = models.DateTimeField(blank=True ,null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

