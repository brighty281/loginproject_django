from django.contrib.auth.hashers import make_password
from django.db import models

# Create your models here.


class register(models.Model):
    username=models.CharField(max_length=250 ,)
    email=models.EmailField()
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.username





