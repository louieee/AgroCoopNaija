# Generated by Django 2.1.4 on 2019-04-23 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0007_auto_20190423_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='cooperative',
            name='phone',
            field=models.CharField(default='', max_length=50),
        ),
    ]
