# Generated by Django 2.1.4 on 2019-04-21 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.CharField(choices=[('L', 'Like'), ('D', 'Dislike'), ('N', 'None')], default='N', max_length=7)),
                ('message_type', models.CharField(choices=[('P', 'Post'), ('C', 'Comment'), ('R', 'Reply'), ('N', 'None')], default='N', max_length=8)),
                ('message_id', models.IntegerField()),
                ('reactor_id', models.IntegerField()),
            ],
        ),
    ]