# Generated by Django 2.1.4 on 2019-06-12 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0005_auto_20190612_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='time_to_pay',
            field=models.DateTimeField(blank=True),
        ),
    ]