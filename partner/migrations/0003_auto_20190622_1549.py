# Generated by Django 2.1.4 on 2019-06-22 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0002_auto_20190523_1928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partner',
            old_name='corporate_name',
            new_name='institution',
        ),
        migrations.AddField(
            model_name='partner',
            name='position',
            field=models.CharField(default='Staff', max_length=255),
        ),
    ]