# Generated by Django 2.0.3 on 2018-03-27 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingapp', '0006_auto_20180327_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mall',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]