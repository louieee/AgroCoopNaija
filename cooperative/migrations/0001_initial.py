# Generated by Django 2.1.4 on 2019-05-10 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collateral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('document', models.FileField(upload_to='attachment/')),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cooperative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('Area_of_Specialization', models.CharField(max_length=255)),
                ('icon', models.ImageField(upload_to='image/')),
                ('website', models.URLField()),
                ('motto', models.CharField(default='', max_length=255)),
                ('phone', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('about', models.TextField()),
                ('reg_no', models.CharField(default='', max_length=100)),
                ('account_name', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=255)),
                ('bank', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='document/')),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
                ('payment_proof', models.ImageField(upload_to='image/')),
                ('verified', models.BooleanField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=50)),
                ('status', models.CharField(choices=[('N', 'New'), ('G', 'Granted'), ('D', 'Declined')], default='N', max_length=10)),
                ('paid', models.BooleanField(default=False)),
                ('time_asked', models.DateTimeField()),
                ('time_granted', models.DateTimeField()),
                ('time_to_pay', models.DateTimeField()),
                ('percentage_of_interest', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
            ],
        ),
    ]
