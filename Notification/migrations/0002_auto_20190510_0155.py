# Generated by Django 2.1.4 on 2019-05-10 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Notification', '0001_initial'),
        ('cooperative', '0002_auto_20190510_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewedneednotification',
            name='need',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Need'),
        ),
        migrations.AddField(
            model_name='viewedneednotification',
            name='notification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notification.Notification'),
        ),
        migrations.AddField(
            model_name='viewedmembershipnotification',
            name='mem_request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cooperative.MembershipRequest'),
        ),
        migrations.AddField(
            model_name='viewedmembershipnotification',
            name='notification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notification.Notification'),
        ),
        migrations.AddField(
            model_name='viewedloannotification',
            name='loan',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Loan'),
        ),
        migrations.AddField(
            model_name='viewedloannotification',
            name='notification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notification.Notification'),
        ),
        migrations.AddField(
            model_name='viewedinvestmentnotification',
            name='investment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Investment'),
        ),
        migrations.AddField(
            model_name='viewedinvestmentnotification',
            name='notification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notification.Notification'),
        ),
        migrations.AddField(
            model_name='notification',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cooperative.Member'),
        ),
    ]