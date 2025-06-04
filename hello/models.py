from django.core.validators import MaxValueValidator
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Inventory(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    gitn = models.CharField(max_length=14)
    counter = models.IntegerField(null=False, blank=False)
    expiry_date_min = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    gitn = models.CharField(max_length=14)
    location = models.CharField(max_length=200)
    buy_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name