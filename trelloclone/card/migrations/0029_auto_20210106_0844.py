# Generated by Django 3.1 on 2021-01-06 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0028_auto_20210106_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(blank=True, default='2021-01-06 08:44:00'),
        ),
    ]
