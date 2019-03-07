# Generated by Django 2.1.4 on 2019-03-05 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('acct_name', models.CharField(max_length=255)),
                ('acct_number', models.CharField(max_length=30)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiver', to='wallet.Wallet'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender', to='wallet.Wallet'),
        ),
    ]