# Generated by Django 3.1.3 on 2020-12-25 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_board_head'),
        ('list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='list_board', to='board.board'),
        ),
    ]