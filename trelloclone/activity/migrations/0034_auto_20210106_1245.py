# Generated by Django 3.1 on 2021-01-06 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0033_auto_20210106_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='created_at',
            field=models.DateTimeField(blank=True, default='2021-01-06 12:45:25'),
        ),
    ]
