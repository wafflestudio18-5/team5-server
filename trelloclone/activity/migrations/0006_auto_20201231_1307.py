# Generated by Django 3.1 on 2020-12-31 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_auto_20201231_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='created_at',
            field=models.DateTimeField(blank=True, default='2020-12-31 13:07:35'),
        ),
    ]
