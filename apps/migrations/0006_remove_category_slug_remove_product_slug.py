# Generated by Django 5.1.6 on 2025-03-15 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
