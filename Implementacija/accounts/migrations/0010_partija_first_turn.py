# Generated by Django 4.0.4 on 2022-05-30 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_potez_idigra_alter_trening_idkor'),
    ]

    operations = [
        migrations.AddField(
            model_name='partija',
            name='first_turn',
            field=models.IntegerField(default=1),
        ),
    ]