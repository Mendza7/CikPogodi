# Generated by Django 4.0.4 on 2022-06-01 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_partija_first_turn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partija',
            name='first_turn',
            field=models.IntegerField(default=0),
        ),
    ]
