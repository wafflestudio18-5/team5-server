# Generated by Django 3.1 on 2020-12-29 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20201227_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='access_type',
            new_name='grantType',
        ),
    ]