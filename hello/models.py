from datetime import timedelta, datetime, date

import uuid
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Min

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Item(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    gtin = models.CharField(max_length=14, unique=True)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    imageurl = models.CharField(max_length=300, null=True, blank=True)
    expiry_date = models.DateField(default=datetime.today)
    count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name.lower()

    def earliest_expiry_date(self):
        result = self.inventories.aggregate(Min('expiry_date'))
        earliest = result['expiry_date__min']
        if earliest:
            self.expiry_date = earliest
            self.save()
        return earliest

    def get_inventory_count_for_item(self):
        count = self.inventories.count()
        self.count = count
        self.save()
        return count


class Inventory(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    gtin = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='inventories')
    location = models.CharField(max_length=200)
    buy_date = models.DateField(default=datetime.today)
    expiry_date = models.DateField(default=date(9999, 12, 31))

    def __str__(self):
        return f"{self.name or ''} {self.location} ({self.gtin.gtin})"

    def get_name(self):
        if self.gtin:
            self.name = self.gtin.name.lower()
            self.save()
            return self.name
        return 'name not found'