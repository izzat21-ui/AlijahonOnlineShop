# Generated by Django 5.1.6 on 2025-03-25 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0008_alter_thread_discount_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
