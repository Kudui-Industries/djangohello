# Generated by Django 4.2.20 on 2025-06-05 11:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_item_rename_expiry_date_inventory_expiry_date_min_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='buy_date',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='item',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
