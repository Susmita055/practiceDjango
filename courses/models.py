from django.db import models
from accounts.models import User


# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    deleted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
