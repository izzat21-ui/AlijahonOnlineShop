# Generated by Django 5.1.6 on 2025-03-26 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment_operator',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
