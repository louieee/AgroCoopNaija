# Generated by Django 2.1.4 on 2019-05-10 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190510_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='', upload_to='image/'),
        ),
    ]
