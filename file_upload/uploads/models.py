from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    designation = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.name
