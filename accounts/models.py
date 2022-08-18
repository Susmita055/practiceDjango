from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
# Create your models here.


class User(AbstractUser):
    phone_number = models.IntegerField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
