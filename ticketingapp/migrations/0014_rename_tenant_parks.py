# Generated by Django 2.1.4 on 2018-12-24 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketingapp', '0013_remove_park_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tenant',
            old_name='parks',
            new_name='park',
        ),
    ]
