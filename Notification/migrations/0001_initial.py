# Generated by Django 2.1.4 on 2019-05-03 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cooperative', '0013_auto_20190503_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Member')),
            ],
        ),
        migrations.CreateModel(
            name='ViewedInvestmentNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment_id', models.IntegerField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Member')),
            ],
        ),
        migrations.CreateModel(
            name='ViewedLoanNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.IntegerField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Member')),
            ],
        ),
        migrations.CreateModel(
            name='ViewedMembershipNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_id', models.IntegerField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Member')),
            ],
        ),
        migrations.CreateModel(
            name='ViewedNeedNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('need_id', models.IntegerField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Member')),
            ],
        ),
    ]