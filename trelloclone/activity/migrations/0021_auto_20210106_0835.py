# Generated by Django 3.1 on 2021-01-06 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0020_auto_20210106_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='created_at',
            field=models.DateTimeField(blank=True, default='2021-01-06 08:35:44'),
        ),
    ]
