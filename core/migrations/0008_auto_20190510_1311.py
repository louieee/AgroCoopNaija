# Generated by Django 2.1.4 on 2019-05-10 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190510_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='', upload_to='image/'),
        ),
    ]
