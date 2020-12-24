# Generated by Django 3.1.3 on 2020-12-24 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('card', '0001_initial'),
        ('list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_list', to='list.list'),
        ),
        migrations.AddField(
            model_name='card',
            name='prev',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='next', to='card.card'),
        ),
    ]
