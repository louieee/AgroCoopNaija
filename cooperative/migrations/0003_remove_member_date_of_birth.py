# Generated by Django 2.1.4 on 2019-04-21 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0002_auto_20190421_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='date_of_birth',
        ),
    ]
