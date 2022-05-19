# Generated by Django 4.0.4 on 2022-05-19 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_potez_slovo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='potez',
            name='idigra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.igra'),
        ),
        migrations.AlterField(
            model_name='trening',
            name='idkor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
