# Generated by Django 4.0.3 on 2022-11-28 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0002_vendor_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
