from django.contrib import admin
from .models import Inventory
from .models import Item
from .models import Task
# Register your models here.

admin.site.register(Inventory)
admin.site.register(Item)
admin.site.register(Task)