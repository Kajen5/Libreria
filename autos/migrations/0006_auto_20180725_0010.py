# Generated by Django 2.0.5 on 2018-07-25 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0005_auto_20180724_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='id_reserva',
        ),
        migrations.AddField(
            model_name='reserva',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
