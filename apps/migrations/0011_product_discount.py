# Generated by Django 5.1.6 on 2025-03-26 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_order_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
