# Generated by Django 4.0.dev20210722095828 on 2021-08-04 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_remove_employeetimelog_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeetimelog',
            old_name='date',
            new_name='date_time',
        ),
    ]