# Generated by Django 2.1.4 on 2019-06-07 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0003_auto_20190603_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(choices=[('Committee Member', 'Committee Member'), ('Member', 'Member')], default='Member', max_length=17),
        ),
    ]