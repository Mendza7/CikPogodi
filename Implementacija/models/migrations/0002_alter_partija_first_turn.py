# Generated by Django 4.0.4 on 2022-06-02 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partija',
            name='first_turn',
            field=models.IntegerField(default=0),
        ),
    ]
