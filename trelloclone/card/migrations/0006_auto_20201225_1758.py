# Generated by Django 3.1.3 on 2020-12-25 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0005_auto_20201225_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='prev',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='next', to='card.card'),
        ),
    ]
