# Generated by Django 2.1.4 on 2019-06-13 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0008_auto_20190613_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='verified',
            field=models.BooleanField(default=None, null=True),
        ),
    ]