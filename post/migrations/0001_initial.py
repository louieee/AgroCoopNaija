# Generated by Django 2.1.4 on 2019-04-21 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachment/')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.IntegerField()),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.IntegerField()),
                ('date_posted', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, upload_to='image/')),
                ('video', models.URLField(blank=True)),
                ('tag', models.CharField(default='animal husbandry', max_length=255)),
                ('audio', models.URLField(blank=True)),
                ('for_cooperative', models.BooleanField(default=False)),
                ('cooperative_name', models.CharField(blank=True, max_length=255)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.IntegerField()),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Comment')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
    ]
