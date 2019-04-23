# Generated by Django 2.1.4 on 2019-04-21 15:20

import builtins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('cooperative', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=builtins.id, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('date_of_birth', models.DateField()),
                ('time_of_request', models.DateTimeField()),
                ('date_of_admission', models.DateTimeField(blank=True)),
                ('account_name', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=255)),
                ('bank', models.CharField(max_length=255)),
                ('cooperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Cooperative')),
            ],
        ),
        migrations.CreateModel(
            name='MembershipRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_id', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('time_of_request', models.DateTimeField()),
                ('cooperative_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Cooperative')),
            ],
        ),
        migrations.CreateModel(
            name='Need',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=50)),
                ('time', models.DateTimeField()),
                ('cooperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Cooperative')),
            ],
        ),
        migrations.AddField(
            model_name='loan',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Member'),
        ),
        migrations.AddField(
            model_name='investment',
            name='investor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Member'),
        ),
        migrations.AddField(
            model_name='investment',
            name='need',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Need'),
        ),
        migrations.AddField(
            model_name='document',
            name='cooperative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Cooperative'),
        ),
        migrations.AddField(
            model_name='collateral',
            name='Loan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Loan'),
        ),
    ]