# Generated by Django 3.0.11 on 2021-01-29 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lenme', '0002_auto_20210129_1830'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='Interest',
            new_name='interest',
        ),
    ]
