# Generated by Django 3.1 on 2021-01-06 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0038_auto_20210106_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(blank=True, default='2021-01-06 16:50:57'),
        ),
    ]
