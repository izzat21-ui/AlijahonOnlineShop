# Generated by Django 5.1.6 on 2025-03-26 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0013_alter_order_comment_operator'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='send_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
