# Generated by Django 4.2.20 on 2025-06-06 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_item_order_alter_item_buy_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='gitn',
            new_name='gtin',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='gitn',
            new_name='gtin',
        ),
    ]
